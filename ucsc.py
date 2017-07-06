import os
import MySQLdb
import argparse

class Annotation(object):
    """Query UCSC genome browser with genomic intervals,
    return list with gene names.

    A list of genes can be passed to filter genes of interest.

    """

    def __init__(self, host=None, user=None, passwd=None, db=None,
                 genefile=None, genes=None):
        if host is None:
            host = 'genome-mysql.cse.ucsc.edu'
        if user is None:
            user = 'genome'
        if passwd is None:
            passwd = ''
        if db is None:
            db = 'hg19'
        if genefile is not None:
            self.genes = self._genelist(genefile)
        elif genefile is None and genes is None:
            self.genes = None
        elif genefile is None and genes is not None:
            self.genes = genes

        self.host = host
        self.user = user
        self.db = db
        self.passwd = passwd
        self.conn, self.c = self._ucsc_connect()

    def _ucsc_connect(self):
        conn = MySQLdb.connect(host=self.host, user=self.user,
                               passwd=self.passwd, db=self.db)
        c = conn.cursor()
        return conn, c

    def _ucsc_disconnect(self, conn):
        conn.close()

    def _genelist(self, gf):
        with open(gf, 'r') as f:
            return [line.strip() for line in f]

    def get_genename(self, chromosome, start, end, tx=True, cds=False):
        if cds:
            tx = False

        txsql = """SELECT DISTINCT name2
        FROM refGene
        WHERE chrom='{c}' AND
        ('{s}'<txEnd AND '{s}'>txStart) AND
        ('{e}'<txEnd AND '{e}'>txStart)
        """.format(c=chromosome, s=start, e=end)

        cdssql = """SELECT DISTINCT name2
        FROM refGene
        WHERE chrom='{c}' AND
        ('{s}'<cdsEnd AND '{s}'>cdsStart) AND
        ('{e}'<cdsEnd AND '{e}'>cdsStart)
        """.format(c=chromosome, s=start, e=end)

        if tx and not cds:
            self.c.execute(txsql)
        elif cds and not tx:
            self.c.execute(cdssql)

        if self.c.rowcount != 0:
            out = self.c.fetchall()
            if len(out) == 1:
                return out[0][0]
            elif len(out) > 1 and self.genes is None:
                return [tup[0] for tup in out]
            elif len(out) > 1 and self.genes is not None:
                out = [tup[0] for tup in out if tup[0] in self.genes]
                return out[0]
        elif self.c.rowcount == 0:
            return 'EXTRA_REGIO'

    def parse_bed_file(self, bed):
        bedname = os.path.splitext(bed)[0]
        with open(bed, 'r') as f, open('{}.annotated'.format(bedname), 'w') as fout:
            for line in f:
                chromosome, start, end = line.split()
                genename = self.get_genename(chromosome, int(start) + 21, int(end) - 20)
                fout.write('{}\t{}\t{}\t{}\n'.format(chromosome, start, end, genename))


def get_arguments():
    """Parse arguments and return Namespace object."""

    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bed", type=str, metavar='',
                        help="BED file",  required=True)
    parser.add_argument("-g", "--genelist", type=str, metavar='',
                        help="File with gene names")

    return parser.parse_args()

def main():
    args = get_arguments()
    print('Annotating {} @ UCSC'.format(args.bed))
    if args.genelist:
        Annotation(genefile=args.genelist).parse_bed_file(args.bed)
    elif not args.genelist:
        Annotation().parse_bed_file(args.bed)

if __name__ == '__main__':
    main()
