import csv
import datetime
import hashlib
import os

from dpkt import ethernet, ip, ip6
from dpkt.utils import inet_to_str
from .pcap_extractor.mail import Mail
from .pcap_extractor.TCPFlow import TCPFlow
from .pcap_extractor.DNSExtractor import DNSItem
from .pcap_extractor.HTTPParser import HttpData
from abc import ABCMeta, abstractmethod


class DictSerializable(object):
    """
    可序列化为字典的类的基类 => 继承本抽象类的类拥有序列化成字典的能力
    """
    __metaclass__ = ABCMeta  # 指定这是一个抽象类

    @abstractmethod
    def toDict(self) -> dict:
        pass


class TCPMixin(DictSerializable):
    """
    TCP记录，所有继承本类的记录都拥有记录TCP属性的功能
    """

    def __init__(self):
        self.srcIP = ""
        self.srcPort = 0
        self.dstIP = ""
        self.dstPort = 0

    def setTCP(self, tcpFlow: TCPFlow):
        self.srcIP = tcpFlow.srcIP
        self.srcPort = tcpFlow.srcPort
        self.dstIP = tcpFlow.dstIP
        self.dstPort = tcpFlow.dstPort

    def toDict(self) -> dict:
        return {
            "srcIP": self.srcIP,
            "srcPort": self.srcPort,
            "dstIP": self.dstIP,
            "dstPort": self.dstPort
        }


class IPMixin(DictSerializable):
    """
    IP记录，所有继承本类的记录都拥有记录IP地址的功能
    """

    def __init__(self):
        self.srcIP = ""
        self.dstIP = ""

    def setIP(self, ethPacket: ethernet.Ethernet):
        ipPacket = ethPacket.data
        self.srcIP = inet_to_str(ipPacket.src)
        self.dstIP = inet_to_str(ipPacket.dst)

    def toDict(self) -> dict:
        return {
            "srcIP": self.srcIP,
            "dstIP": self.dstIP
        }


class RecordBase(DictSerializable):
    """
    所有报告记录的基类
    """

    # class ObservableItem(dict, DictSerializable):
    #     def toDict(self) -> dict:
    #         return self

    # def __init__(self, observableId: str, observableType: str):
    #     self.observableId = observableId
    #     self.observableType = observableType
    #
    # def toDict(self) -> dict:
    #     return {
    #         "observableId": self.observableId,
    #         "observableType": self.observableType
    #     }

    __metaclass__ = ABCMeta  # 指定这是一个抽象类

    def __init__(self):
        self.observables = []

    def setObservables(self, observables: [dict]):
        self.observables = observables

    def toDict(self) -> dict:
        return {
            "observables": self.observables
        }


class FileHash(DictSerializable):
    """
    表示文件Hash值
    """

    def __init__(self, data: bytes = None):
        if data:
            self.md5 = hashlib.md5(data).hexdigest()
            self.sha1 = hashlib.sha1(data).hexdigest()
            self.sha256 = hashlib.sha256(data).hexdigest()
        else:
            self.md5 = ""
            self.sha1 = ""
            self.sha256 = ""

    def toDict(self) -> dict:
        return {
            "md5": self.md5,
            "sha1": self.sha1,
            "sha256": self.sha256
        }


class FileItem(DictSerializable):
    """
    文件条目
    """

    def __init__(self, fileData: bytes, filename: str = "", fileType: str = ""):
        self.filename = filename,
        self.fileType = fileType,
        self.fileHash = FileHash(fileData)

    def toDict(self) -> dict:
        return {
            "filename": self.filename,
            "fileType": self.fileType,
            "fileHash": self.fileHash.toDict()
        }


class EmailRecord(RecordBase, TCPMixin):
    """
    Email记录
    """

    def __init__(self):
        super().__init__()
        self.plain = ""  # 消息内容
        self.html = ""  # html格式的内容
        self.From = ""  # 发件人地址
        self.To = ""  # 收件人地址
        self.Cc = ""  # 抄送地址
        # self.Date = ""  # 日期和时间
        self.Subject = ""  # 主题
        self.MessageID = ""  # 消息ID
        self.files = []

    def initByMailAndObservable(self, mail: Mail):
        self.plain = mail.plain
        if isinstance(self.plain, bytes):
            self.plain = self.plain.decode()
        self.html = mail.html
        self.From = mail.From
        self.To = mail.To
        self.Cc = mail.Cc
        # self.Date = mail.Date
        self.Subject = mail.Subject
        self.MessageID = mail.MessageID
        for mailFile in mail.files:
            self.files.append(FileItem(mailFile.fileData, mailFile.fileName, mailFile.fileType))

    def toDict(self) -> dict:
        filesDict = []
        for file in self.files:
            filesDict.append(file.toDict())
        return {
            "plain": self.plain,
            "html": self.html,
            "from": self.From,
            "to": self.To,
            "cc": self.Cc,
            # "date": self.Date,
            "subject": self.Subject,
            "messageId": self.MessageID,
            "files": filesDict,
            **RecordBase.toDict(self),
            **TCPMixin.toDict(self)
        }


class DNSRecord(RecordBase, IPMixin):
    """
    DNS解析记录
    """

    def __init__(self):
        super().__init__()
        self.domain = ""
        self.domain_type = ""
        self.value = ""
        self.timestamp = 0

    def initByDNSItem(self, item: DNSItem):
        self.domain = item.domain
        self.domain_type = item.domain_type
        self.value = item.value
        self.timestamp = item.timestamp
        self.setIP(item.ethPacket)

    def toDict(self) -> dict:
        return {
            "domain": self.domain,
            "domain_type": self.domain_type,
            "value": self.value,
            "timestamp": self.timestamp,
            **RecordBase.toDict(self),
            **IPMixin.toDict(self)
        }


class HTTPRecord(RecordBase, TCPMixin):
    """
    HTTP记录
    """

    class HttpRequest(DictSerializable):
        """
        HTTP请求记录
        """

        def __init__(self, httpData: HttpData):
            self.uri = httpData.request.uri
            self.method = httpData.request.method
            self.headers = httpData.request.headers
            self.version = httpData.request.version
            self.domain = httpData.getDomain()
            self.url = httpData.getUrl()

        def toDict(self) -> dict:
            return {
                "uri": self.uri,
                "method": self.method,
                "headers": self.headers,
                "version": self.version,
                "domain": self.domain,
                "url": self.url
            }

    class HttpResponse(DictSerializable):
        """
        HTTP响应记录
        """

        def __init__(self, httpData: HttpData):
            self.status = httpData.response.status
            self.reason = httpData.response.reason
            self.body = httpData.response.body
            self.headers = httpData.response.headers
            self.version = httpData.response.version

        def toDict(self) -> dict:
            return {
                "status": self.status,
                "reason": self.reason,
                # "body": self.body,
                "headers": self.headers,
                "version": self.version
            }

    def __init__(self, httpData: HttpData):
        super().__init__()
        self.request = HTTPRecord.HttpRequest(httpData)
        self.response = HTTPRecord.HttpResponse(httpData)

    def toDict(self) -> dict:
        return {
            "request": self.request.toDict(),
            "response": self.response.toDict(),
            **RecordBase.toDict(self),
            **TCPMixin.toDict(self)
        }


class FTPRecord(RecordBase, TCPMixin):
    """
    FTP 记录
    """

    def __init__(self, data: bytes = None):
        super().__init__()
        self.fileHash = None
        if data:
            self.fileHash = FileHash(data)

    def toDict(self) -> dict:
        return {
            "fileHash": self.fileHash.toDict(),
            **RecordBase.toDict(self),
            **TCPMixin.toDict(self)
        }


class Report(DictSerializable):
    """
    对比报告
    """

    def toDict(self) -> dict:
        emailRecordsDict = []
        ftpRecordsDict = []
        httpRecordsDict = []
        domainRecordsDict = []
        for emailRecord in self.emailRecords:
            emailRecordsDict.append(emailRecord.toDict())
        for ftpRecord in self.ftpRecords:
            ftpRecordsDict.append(ftpRecord.toDict())
        for httpRecord in self.httpRecords:
            httpRecordsDict.append(httpRecord.toDict())
        for domainRecord in self.domainRecords:
            domainRecordsDict.append(domainRecord.toDict())
        return {
            "totalPacket": self.totalPacket,
            "totalIPAddress": self.totalIPAddress,
            "totalIPv6Address": self.totalIPv6Address,
            "totalIPPacket": self.totalIPPacket,
            "totalIPv6Packet": self.totalIPv6Packet,
            "duration": self.duration,
            "totalTCPFlowNum": self.totalTCPFlowNum,
            "totalHTTPNum": self.totalHTTPNum,
            "totalFTPNum": self.totalFTPNum,
            "totalEmailNum": self.totalEmailNum,
            "totalFileNum": self.totalFileNum,
            "totalDomainNum": self.totalDomainNum,
            "totalMatchIpAddress": self.totalMatchIpAddress,
            "totalMatchIpv6Address": self.totalMatchIpv6Address,
            "totalMatchEmailNum": self.totalMatchEmailNum,
            "totalMatchDomain": self.totalMatchDomain,
            "totalMatchFileHash": self.totalMatchFileHash,
            "totalMatchUri": self.totalMatchUri,
            "startTime": self.startTime,
            "endTime": self.endTime,
            "emailRecords": emailRecordsDict,
            "ftpRecords": ftpRecordsDict,
            "httpRecords": httpRecordsDict,
            "domainRecords": domainRecordsDict
        }

    def __init__(self):
        self.totalPacket = 0  # Total packet num in pcap file
        self.totalIPAddress = 0  # Total ipv4 address num in pcap file
        self.totalIPv6Address = 0  # Total ipv6 address num in pcap file
        self.totalIPPacket = 0  # Total ipv4 packet num in pcap file
        self.totalIPv6Packet = 0  # Total ipv6 pcaket num in pcap file
        self.duration = 0  # The duration between the begin of pcap file and end of pcap file
        self.totalTCPFlowNum = 0  # Total TCP flow num in pcap file
        self.totalHTTPNum = 0  # Total HTTP session num in pcap file
        self.totalFTPNum = 0  # Total FTP session num in pcap file
        self.totalEmailNum = 0  # Total email num in pcap file，contain SMTP、POP3 and IMAP protocol
        self.totalFileNum = 0  # Total file num extract from pcap file, from FTP、SMTP、POP3 、IMAP and HTTP
        self.totalDomainNum = 0  # Total domain num extract from DNS query and DNS response）

        self.totalMatchIpAddress = 0  # Total ipv4 address matched
        self.totalMatchIpv6Address = 0  # Total ipv6 address matched
        self.totalMatchEmailNum = 0  # Total email matched
        self.totalMatchDomain = 0  # Total domain matched
        self.totalMatchFileHash = 0  # Total file hash matched
        self.totalMatchUri = 0  # Total match uri

        self.emailRecords = []  # contain all email which some observable match it
        self.ftpRecords = []  # contain all FTP session which some observable match it
        self.httpRecords = []  # contain all HTTP session which some observable match it
        self.domainRecords = []  # contain all Domain query record which some observable match it

        self.isFirst = True
        self.isDumpCsv = True
        self.ipv4AddressSet = set()
        self.ipv6AddressSet = set()
        self.startTime = 0
        self.endTime = 0
        self.outputCsvDir = "outputcsv"

        self.ipAddressCSVFile = None
        self.emailAddressCSVFile = None
        self.uriCSVFile = None
        self.fileHashCSVFile = None
        self.domainCSVFile = None

        self.ipAddressCSVWriter = None
        self.emailAddressCSVWriter = None
        self.uriCSVWriter = None
        self.fileHashCSVWriter = None
        self.domainCSVWriter = None

    def begin(self):
        """
        报告开始
        :return:
        """
        if self.isDumpCsv:
            if not os.path.exists(self.outputCsvDir):
                os.makedirs(self.outputCsvDir)
            self.ipAddressCSVFile = open(f"{self.outputCsvDir}/ipAddress.csv", "w")
            self.emailAddressCSVFile = open(f"{self.outputCsvDir}/emailAddress.csv", "w")
            self.uriCSVFile = open(f"{self.outputCsvDir}/uri.csv", "w")
            self.fileHashCSVFile = open(f"{self.outputCsvDir}/fileHash.csv", "w")
            self.domainCSVFile = open(f"{self.outputCsvDir}/domain.csv", "w")

            self.ipAddressCSVWriter = csv.writer(self.ipAddressCSVFile)
            self.ipAddressCSVWriter.writerow(
                ["srcIP", "dstIP", "value", "occur time", "observable id",
                 "observable upload time"])

            self.emailAddressCSVWriter = csv.writer(self.emailAddressCSVFile)
            self.emailAddressCSVWriter.writerow(
                ["srcIP", "dstIP", "srcPort", "srcPort", "value", "occur time", "observable id",
                 "observable upload time"]
            )
            self.uriCSVWriter = csv.writer(self.uriCSVFile)
            self.uriCSVWriter.writerow(
                ["srcIP", "dstIP", "srcPort", "srcPort", "value", "occur time", "observable id",
                 "observable upload time"]
            )
            self.fileHashCSVWriter = csv.writer(self.fileHashCSVFile)
            self.fileHashCSVWriter.writerow(
                ["srcIP", "dstIP", "srcPort", "srcPort", "md5", "sha1", "sha256", "occur time", "observable id",
                 "observable upload time"]
            )
            self.domainCSVWriter = csv.writer(self.domainCSVFile)
            self.domainCSVWriter.writerow(
                ["srcIP", "dstIP", "value", "occur time", "observable id",
                 "observable upload time"]
            )

    def end(self):
        """
        报告结束
        :return:
        """
        if self.isDumpCsv:
            self.ipAddressCSVFile.close()
            self.emailAddressCSVFile.close()
            self.uriCSVFile.close()
            self.fileHashCSVFile.close()

    def addPacket(self, ethPacket: ethernet.Ethernet, timestamp: float):
        """
        每解析到一个以太网包，
        :return:
        """
        if self.isFirst:
            self.startTime = timestamp
            self.isFirst = False
        self.endTime = timestamp
        self.duration = self.endTime - self.startTime

        self.totalPacket += 1
        ipPacket = ethPacket.data
        if isinstance(ethPacket.data, ip.IP):
            # 如果是 IPv4 包
            self.totalIPPacket += 1
            self.ipv4AddressSet.add(inet_to_str(ipPacket.src))
            self.ipv4AddressSet.add(inet_to_str(ipPacket.dst))
            self.totalIPAddress = len(self.ipv4AddressSet)
        elif isinstance(ethPacket.data, ip6.IP6):
            self.totalIPv6Packet += 1
            self.ipv6AddressSet.add(inet_to_str(ipPacket.src))
            self.ipv6AddressSet.add(inet_to_str(ipPacket.dst))
            self.totalIPv6Address = len(self.ipv6AddressSet)
        else:
            return False

    def addTCPFlow(self, tcpFlow: TCPFlow):
        """
        每解析到一个 TCP 流就调用本回调
        :param tcpFlow:
        :return:
        """
        self.totalTCPFlowNum += 1

    def addEmail(self, mail: Mail, tcpFlow: TCPFlow, observables: [dict]):
        """
        每解析到一个 Email，就调用本方法
        :param observables:
        :param mail:
        :param tcpFlow:
        :return:
        """
        self.totalEmailNum += 1
        self.totalFileNum += len(mail.files)
        if len(observables) <= 0:
            return
        self.addObservable(observables, tcpFlow=tcpFlow)
        emailRecord = EmailRecord()
        emailRecord.initByMailAndObservable(mail)
        emailRecord.setTCP(tcpFlow)
        emailRecord.setObservables(observables)
        self.emailRecords.append(emailRecord)

    def addDNSRecord(self, item: DNSItem, observables: [dict]):
        """
        每解析到一个 DNSRecord，就调动本方法
        :param observables:
        :param item:
        :return:
        """
        self.totalDomainNum += 1
        if len(observables) <= 0:
            return
        self.addObservable(observables, dnsItem=item)
        dnsRecord = DNSRecord()
        dnsRecord.initByDNSItem(item)
        dnsRecord.setObservables(observables)
        self.domainRecords.append(dnsRecord)

    def addHttp(self, httpData: HttpData, tcpFlow: TCPFlow, observables: [dict]):
        """
        每解析到一个 HttpData，就调用本方法
        :param observables:
        :param httpData:
        :param tcpFlow:
        :return:
        """
        self.totalHTTPNum += 1
        if len(observables) <= 0:
            return
        self.addObservable(observables, tcpFlow=tcpFlow)
        httpRecord = HTTPRecord(httpData)
        httpRecord.setTCP(tcpFlow)
        httpRecord.setObservables(observables)
        self.httpRecords.append(httpRecord)

    def addFTP(self, fileHash: FileHash, tcpFlow: TCPFlow, observables: [dict]):
        """
        每解析到一个 FTP 文件，就调用本方法
        :param fileHash:
        :param observables:
        :param tcpFlow:
        :return:
        """
        self.totalFTPNum += 1
        if len(observables) <= 0:
            return
        self.addObservable(observables, tcpFlow=tcpFlow)
        ftpRecord = FTPRecord()
        ftpRecord.fileHash = fileHash
        ftpRecord.setTCP(tcpFlow)
        ftpRecord.setObservables(observables)
        self.ftpRecords.append(ftpRecord)

    def _appendIpAddressCSV(self, observable: dict, tcpFlow: TCPFlow = None, dnsItem: DNSItem = None):
        # "srcIP", "dstIP", "value", "occur time", "observable id", "observable upload time"
        srcIP, dstIP, occurTime = "", "", 0
        if tcpFlow:
            srcIP = tcpFlow.srcIP
            dstIP = tcpFlow.dstIP
            occurTime = datetime.datetime.fromtimestamp(tcpFlow.lastTime).strftime('%Y-%m-%d %H:%M:%S')
        elif dnsItem:
            ipPacket = dnsItem.ethPacket.data
            srcIP = inet_to_str(ipPacket.src)
            dstIP = inet_to_str(ipPacket.dst)
            occurTime = datetime.datetime.fromtimestamp(dnsItem.timestamp).strftime('%Y-%m-%d %H:%M:%S')
        else:
            return

        self.ipAddressCSVWriter.writerow([srcIP, dstIP, observable["value"], f"{occurTime}", observable["stix_id"],
                                          datetime.datetime.fromtimestamp(observable["create_time"]).strftime(
                                              '%Y-%m-%d %H:%M:%S')])

    def _appendEmailAddressCSV(self, observable: dict, tcpFlow: TCPFlow = None):
        # "srcIP", "dstIP", "srcPort", "srcPort", "value", "occur time", "observable id", "observable upload time"
        self.emailAddressCSVWriter.writerow([tcpFlow.srcIP, tcpFlow.dstIP, f"{tcpFlow.srcPort}", f"{tcpFlow.dstPort}",
                                             observable["value"],
                                             datetime.datetime.fromtimestamp(tcpFlow.lastTime).strftime(
                                                 '%Y-%m-%d %H:%M:%S'), observable["stix_id"],
                                             datetime.datetime.fromtimestamp(observable["create_time"]).strftime(
                                                 '%Y-%m-%d %H:%M:%S')])

    def _appendUriCSV(self, observable: dict, tcpFlow: TCPFlow = None):
        # "srcIP", "dstIP", "srcPort", "srcPort", "value", "occur time", "observable id", "observable upload time"
        self.uriCSVWriter.writerow([
            tcpFlow.srcIP, tcpFlow.dstIP, f"{tcpFlow.srcPort}", f"{tcpFlow.dstPort}",
            observable["value"],
            datetime.datetime.fromtimestamp(tcpFlow.lastTime).strftime(
                '%Y-%m-%d %H:%M:%S'), observable["stix_id"],
            datetime.datetime.fromtimestamp(observable["create_time"]).strftime(
                '%Y-%m-%d %H:%M:%S')
        ])

    def _appendFileHashCSV(self, observable: dict, tcpFlow: TCPFlow = None):
        # "srcIP", "dstIP", "srcPort", "srcPort", "md5", "sha1", "sha256", "occur time", "observable id",
        # "observable upload time"
        self.fileHashCSVWriter.writerow([
            tcpFlow.srcIP, tcpFlow.dstIP, f"{tcpFlow.srcPort}", f"{tcpFlow.dstPort}",
            observable["md5"], observable["sha1"], observable["sha256"],
            datetime.datetime.fromtimestamp(tcpFlow.lastTime).strftime(
                '%Y-%m-%d %H:%M:%S'), observable["stix_id"],
            datetime.datetime.fromtimestamp(observable["create_time"]).strftime(
                '%Y-%m-%d %H:%M:%S')
        ])

    def _appendDomainCSV(self, observable: dict, tcpFlow: TCPFlow = None, dnsItem: DNSItem = None):
        # "srcIP", "dstIP", "value", "occur time", "observable id", "observable upload time"
        srcIP, dstIP, occurTime = "", "", 0
        if tcpFlow:
            srcIP = tcpFlow.srcIP
            dstIP = tcpFlow.dstIP
            occurTime = datetime.datetime.fromtimestamp(tcpFlow.lastTime).strftime('%Y-%m-%d %H:%M:%S')
        elif dnsItem:
            ipPacket = dnsItem.ethPacket.data
            srcIP = inet_to_str(ipPacket.src)
            dstIP = inet_to_str(ipPacket.dst)
            occurTime = datetime.datetime.fromtimestamp(dnsItem.timestamp).strftime('%Y-%m-%d %H:%M:%S')
        else:
            return
        self.domainCSVWriter.writerow([
            srcIP, dstIP, observable["value"], occurTime, observable["stix_id"],
            datetime.datetime.fromtimestamp(observable["create_time"]).strftime(
                '%Y-%m-%d %H:%M:%S')
        ])

    def addObservable(self, observables: [dict], tcpFlow: TCPFlow = None, dnsItem: DNSItem = None):
        """
        统计收到的 Observable 信息
        :param dnsItem:
        :param tcpFlow:
        :param observables:
        :return:
        """
        for observable in observables:
            if observable['observableType'] == 'address':
                if observable['type'] == 'ipv4-addr':
                    # ipv4
                    self.totalMatchIpAddress += 1
                    self._appendIpAddressCSV(observable, tcpFlow, dnsItem)
                elif observable['type'] == 'ipv6-addr':
                    # ipv6
                    self.totalMatchIpv6Address += 1
                    self._appendIpAddressCSV(observable, tcpFlow, dnsItem)
                elif observable['type'] == 'e-mail':
                    # email
                    self._appendEmailAddressCSV(observable, tcpFlow)
                    self.totalMatchEmailNum += 1
            elif observable['observableType'] == 'domain':
                # domain
                self._appendDomainCSV(observable, tcpFlow, dnsItem)
                self.totalMatchDomain += 1
            elif observable['observableType'] == 'uri':
                # uri
                self._appendUriCSV(observable, tcpFlow)
                self.totalMatchUri += 1
            elif observable['observableType'] == 'fileHash':
                # file hash
                self._appendFileHashCSV(observable, tcpFlow)
                self.totalMatchFileHash += 1
