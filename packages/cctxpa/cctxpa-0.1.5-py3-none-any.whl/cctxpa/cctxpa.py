import argparse
import datetime
import json
import os
import sys
import dpkt
import requests

from .pcap_extractor.MyEncoder import MyEncoder
from .pcap_extractor.FlowExtractor import FlowExtractor
from .pcap_extractor.TCPFlow import TCPFlow
from .pcap_extractor.mail import Mail
from .pcap_extractor.HTTPParser import HTTPParser, HttpData
from .pcap_extractor.SMTPParser import SMTPParser
from .pcap_extractor.POP3Parser import POP3Parser
from .pcap_extractor.IMAPParser import IMAPParser
from .pcap_extractor.DNSExtractor import DNSExtractor, DNSItem
from .report import Report, FileHash
from progress.bar import Bar
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from rich.columns import Columns
from rich.panel import Panel


class CCTXPcapAnalyser:
    def __init__(self, args):
        self.host = args.host
        self.path = args.path
        self.port = args.port
        self.https = args.https
        self.username = args.username
        self.password = args.password
        self.inputFile = args.pcapfile
        self.outputFile = args.outputfile
        self.progress = args.progress
        if self.port == -1:
            # 不指定端口，使用默认的80或者443
            if self.https:
                self.port = 443
            else:
                self.port = 80

        self.flowExtractor = FlowExtractor(valueCallback=self.dealStream)
        self.dnsExtractor = DNSExtractor(valueCallback=self.dealDNSRecord)
        self.httpParser = HTTPParser()
        self.smtpParser = SMTPParser()
        self.pop3Parser = POP3Parser()
        self.imapParser = IMAPParser()

        self.report = Report()
        self.report.outputCsvDir = args.outputcsvdirectory
        self.url = f'{"https" if self.https else "http"}://{self.host}:{self.port}{self.path}'
        self.registerUrl = f'{self.url}/user/register'
        self.loginUrl = f'{self.url}/user/login'
        self.queryUrl = f'{self.url}/user/queryObservables'
        self.token = ""
        self.refreshToken = ""
        self.report.begin()

    def doAuthGet(self, url: str, params: dict):
        r = requests.get(url, params=params, headers={
            "Authorization": f"Bearer {self.token}"
        })
        responseData = r.json()
        if responseData == 401:
            # 如果权限验证过期，重新登录
            self.doLogin()
            return self.doAuthGet(url, params)
        return responseData

    def doAuthPost(self, url: str, jsonData: dict):
        r = requests.post(url, json=jsonData, headers={
            "Authorization": f"Bearer {self.token}"
        })
        responseData = r.json()
        if responseData == 401:
            # 如果权限验证过期，重新登录
            self.doLogin()
            return self.doAuthPost(url, jsonData)
        return responseData

    @staticmethod
    def buildQueryDomain(domain: str) -> dict:
        return {
            'queryType': 'domain',
            'value': domain
        }

    @staticmethod
    def buildQueryAddress(address: str) -> dict:
        return {
            'queryType': 'address',
            'value': address
        }

    @staticmethod
    def buildQueryUri(uri: str) -> dict:
        return {
            'queryType': 'uri',
            'value': uri
        }

    @staticmethod
    def buildQueryFileHash(fileHash: FileHash) -> dict:
        return {
            'queryType': 'fileHash',
            'md5': fileHash.md5,
            'sha1': fileHash.sha1,
            'sha256': fileHash.sha256
        }

    def doQuery(self, queryItems: [dict]) -> [dict]:
        response = self.doAuthGet(self.queryUrl, params={
            'queries': json.dumps(queryItems),
        })
        if response['code'] == 200:
            if response['data'] and len(response['data']) > 0:
                return response['data']
        else:
            print(f'Query Observable failed, {response["msg"]}')
        return []

    def dealDNSRecord(self, dnsRecord: DNSItem):
        """
        处理每个提取到的 DNS 解析记录
        :param dnsRecord:
        :return:
        """
        # query DNSItem
        observables = self.doQuery([
            CCTXPcapAnalyser.buildQueryDomain(dnsRecord.domain),
            CCTXPcapAnalyser.buildQueryAddress(dnsRecord.value)
        ])
        self.report.addDNSRecord(dnsRecord, observables)

    def dealMail(self, mail: Mail, tcpFlow: TCPFlow):
        # query email address, ip address, file hash
        queryTask = [
            CCTXPcapAnalyser.buildQueryAddress(tcpFlow.srcIP),
            CCTXPcapAnalyser.buildQueryAddress(tcpFlow.dstIP),
            CCTXPcapAnalyser.buildQueryAddress(mail.From),
            CCTXPcapAnalyser.buildQueryAddress(mail.To),
        ]
        for mailFile in mail.files:
            fileHash = FileHash(mailFile.fileData)
            queryTask.append(CCTXPcapAnalyser.buildQueryFileHash(fileHash))
        observables = self.doQuery(queryTask)
        self.report.addEmail(mail, tcpFlow, observables)

    def dealHttpData(self, httpData: HttpData, tcpFlow: TCPFlow):
        # query url, file hash, ip address, domain
        queryTask = [
            CCTXPcapAnalyser.buildQueryAddress(httpData.getDomain()),
            CCTXPcapAnalyser.buildQueryUri(httpData.getUrl()),
            CCTXPcapAnalyser.buildQueryAddress(tcpFlow.srcIP),
            CCTXPcapAnalyser.buildQueryAddress(tcpFlow.dstIP),
        ]
        if httpData.fileHashes:
            fileHash = FileHash()
            fileHash.md5 = httpData.fileHashes["md5"]
            fileHash.sha1 = httpData.fileHashes["sha1"]
            fileHash.sha256 = httpData.fileHashes["sha256"]
            queryTask.append(CCTXPcapAnalyser.buildQueryFileHash(fileHash))
        observables = self.doQuery(queryTask)
        self.report.addHttp(httpData, tcpFlow, observables)

    def dealFTP(self, data: bytes, tcpFlow: TCPFlow):
        fileHash = FileHash(data)
        queryTask = [
            CCTXPcapAnalyser.buildQueryFileHash(fileHash),
            CCTXPcapAnalyser.buildQueryAddress(tcpFlow.srcIP),
            CCTXPcapAnalyser.buildQueryAddress(tcpFlow.dstIP),
        ]
        observables = self.doQuery(queryTask)
        self.report.addFTP(fileHash, tcpFlow, observables)

    def dealStream(self, tcpFlow: TCPFlow):
        """
        处理每个提取到的TCP流
        :param tcpFlow:
        :return:
        """
        self.report.addTCPFlow(tcpFlow)
        forwardBytes, reverseBytes = tcpFlow.getAllForwardBytes(), tcpFlow.getAllReverseBytes()
        if tcpFlow.dstPort == 21:
            pass
        elif tcpFlow.srcPort == 20 or tcpFlow.dstPort == 20:
            # 处理 FTP
            data1, data2 = forwardBytes, reverseBytes
            data = data1 if len(data2) == 0 else data2
            if len(data) > 0:
                # md1 = hashlib.md5()
                # md2 = hashlib.md5()
                # md3 = hashlib.md5()
                # with closing(BytesIO(data)) as data:
                #     for line in data.readlines():
                #         md1.update(line)
                #         if line.endswith(b"\r\n"):
                #             md2.update(line[:-2])
                #             md2.update(b'\r')
                #             md3.update(line[:-2])
                #             md3.update(b'\n')
                self.dealFTP(data, tcpFlow)
        elif tcpFlow.dstPort == 143:
            # 处理 IMAP
            for mail in self.imapParser.parse(forwardBytes, reverseBytes):
                self.dealMail(mail, tcpFlow)
        elif tcpFlow.dstPort == 110:
            for mail in self.pop3Parser.parse(reverseBytes):
                self.dealMail(mail, tcpFlow)
        elif tcpFlow.dstPort == 25:
            for mail in self.smtpParser.parse(forwardBytes):
                self.dealMail(mail, tcpFlow)
        elif (len(forwardBytes) == 0 and len(reverseBytes) > 0) or (len(forwardBytes) > 0 and len(reverseBytes) == 0):
            # try to cal file hash for FTP passive mode
            if len(forwardBytes) == 0 and len(reverseBytes) > 0:
                self.dealFTP(reverseBytes, tcpFlow)
            else:
                self.dealFTP(forwardBytes, tcpFlow)
        else:
            # parse http
            for httpData in self.httpParser.parse(forwardBytes, reverseBytes):
                self.dealHttpData(httpData, tcpFlow)

    def doRegister(self):
        r = requests.post(self.registerUrl, json={
            'username': self.username,
            'password': self.password
        })
        return r.json()

    def doLogin(self):
        r = requests.post(self.loginUrl, json={
            'username': self.username,
            'password': self.password
        })
        data = r.json()
        if data['code'] != 200:
            print(f"Login failed, {data['msg']}")
            return False
        self.token = data['data']['token']
        self.refreshToken = data['data']['refresh_token']
        return True

    def start(self):
        """
        Start to parse pcap file
        :return:
        """

        # do login first
        if not self.doLogin():
            return

        if self.progress:
            bar = Bar('Extract Progress:', max=100)
        else:
            bar = None
        with open(self.inputFile, 'rb') as pcap:
            progress = 0
            totalSize = os.path.getsize(self.inputFile)
            packets = dpkt.pcap.Reader(pcap)
            for ts, buf in packets:
                if self.progress:
                    currentProgress = int(pcap.tell() * 100 / totalSize)
                    if currentProgress != progress:
                        progress = currentProgress
                        bar.next()
                ethPacket = dpkt.ethernet.Ethernet(buf)
                self.report.addPacket(ethPacket, ts)
                self.flowExtractor.addPacket(ethPacket, ts)
                self.dnsExtractor.addPacket(ethPacket, ts)
        if self.progress:
            bar.finish()
        self.flowExtractor.done()


def printReport(report: Report, args):
    """
    Print compare report
    :param report:
    :return:
    """

    def getPanelContent(key, value: str = None):
        return Panel(f"[b]{key}[/b]\n[yellow]{getattr(report, key) if value is None else value}", expand=True)

    console = Console()
    console.print(Markdown("# Analyser Report"))
    renderAbles = [
                      getPanelContent('input pcap file', args.pcapfile),
                      getPanelContent('detail report', args.outputfile),
                      getPanelContent('startTime',
                                      datetime.datetime.fromtimestamp(report.startTime).strftime('%Y-%m-%d %H:%M:%S')),
                      getPanelContent('endTime',
                                      datetime.datetime.fromtimestamp(report.endTime).strftime('%Y-%m-%d %H:%M:%S')),
                      getPanelContent('duration', report.endTime - report.startTime),

                  ] + [getPanelContent(item) for item in
                       ['totalPacket', 'totalIPAddress', 'totalIPv6Address', 'totalIPPacket', 'totalIPv6Packet',
                        'totalTCPFlowNum', 'totalHTTPNum', 'totalFTPNum', 'totalEmailNum', 'totalFileNum',
                        'totalDomainNum',
                        'totalMatchIpAddress', 'totalMatchIpv6Address', 'totalMatchEmailNum', 'totalMatchDomain',
                        'totalMatchFileHash', 'totalMatchUri']]
    columns = Columns(renderAbles, equal=True, expand=True)
    console.print(columns)

    console.print(Markdown("## CCTX Observable Match Results"))
    table = Table(expand=True)
    table.add_column("Extracted Feature", justify='center', style='cyan')
    table.add_column("Extracted Feature Count", justify='center', style='cyan')
    table.add_column("Matched Observable Count", justify='center', style='magenta')
    table.add_column("Matching Percentage", justify='center', style='green')
    table.add_row('IPv4 address', f"{report.totalIPAddress}", f"{report.totalMatchIpAddress}",
                  f"{0 if report.totalIPAddress == 0 else round(report.totalMatchIpAddress * 100.0 / report.totalIPAddress, 2)}%")
    table.add_row("IPv6 address", f"{report.totalIPv6Address}", f"{report.totalMatchIpv6Address}",
                  f"{0 if report.totalIPv6Address == 0 else round(report.totalMatchIpv6Address * 100.0 / report.totalIPv6Address, 2)}%")
    table.add_row("Email address", f"{report.totalEmailNum}", f"{report.totalMatchEmailNum}",
                  f"{0 if report.totalEmailNum == 0 else round(report.totalMatchEmailNum * 100.0 / report.totalEmailNum, 2)}%")
    table.add_row("Domain", f"{report.totalDomainNum}", f"{report.totalMatchDomain}",
                  f"{0 if report.totalDomainNum == 0 else round(report.totalMatchDomain * 100.0 / report.totalDomainNum, 2)}%")
    table.add_row("Uri", f"{report.totalHTTPNum}", f"{report.totalMatchUri}",
                  f"{0 if report.totalHTTPNum == 0 else round(report.totalMatchUri * 100.0 / report.totalHTTPNum, 2)}%")
    table.add_row("File hash", f"{report.totalFileNum}", f"{report.totalMatchFileHash}",
                  f"{0 if report.totalFileNum == 0 else round(report.totalMatchFileHash * 100.0 / report.totalFileNum, 2)}%")
    console.print(table)


def main():
    """
    cctxpa is a command lien tool for CCTX to parse pcap file and compare with CCTX's Observables
    """
    if len(sys.argv) == 1:
        sys.argv.append('--help')
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default="127.0.0.1", help="CCTX pcap analyser server addresss")
    parser.add_argument('--port', type=int, default=5000, help="CCTX pcap analyser server port")
    parser.add_argument('--https', action='store_true', help="Use https or http")
    parser.add_argument('--register', action='store_true', help="Just do register account")
    parser.add_argument('--path', type=str, default="", help="CCTX pcap analyser server login path")
    parser.add_argument('--progress', action='store_true',
                        help="Print progress, if open, maybe lead slow extract speed.")
    parser.add_argument('-u', '--username', type=str, required=True, help="Username")
    parser.add_argument('-p', '--password', type=str, required=True, help="Password")
    parser.add_argument('-f', '--pcapfile', type=str, default='test.pcap', help="Pcap file need to parse!")
    parser.add_argument('-o', '--outputfile', type=str, default="report.json", help="A file to store output report")
    parser.add_argument('-ocd', '--outputcsvdirectory', type=str, default='outputcsv',
                        help="A directory to store output csv file")
    args = parser.parse_args()

    cctxpa = CCTXPcapAnalyser(args)
    if args.register:
        # do register
        print(cctxpa.doRegister())
    else:
        cctxpa.start()
        with open(args.outputfile, 'w') as file:
            file.write(json.dumps(cctxpa.report.toDict(), ensure_ascii=False, cls=MyEncoder))
        printReport(cctxpa.report, args)


if __name__ == '__main__':
    main()
