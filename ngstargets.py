import os, sys, time, argparse, logging
import MySQLdb
import time
import pandas as pd
import sqlite3
import json

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
            lines = (line.rstrip() for line in f)
            lines = list(line for line in lines if line)
            return [l.split()[0] for l in lines]

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
                gout = [tup[0] for tup in out if tup[0] in self.genes]
                if len(gout) > 0:
                    return gout[0]
                elif len(gout) == 0:
                    return 'EXTRA_REGIO'
        elif self.c.rowcount == 0:
            return 'EXTRA_REGIO'

    def get_region(self, gene, tx=True, cds=False):
        if cds:
            tx = False

        txsql = """SELECT DISTINCT chrom, txStart, txEnd
        FROM refGene
        WHERE name2='{g}'
        """.format(g=gene)

        cdssql = """SELECT DISTINCT chrom, cdsStart, cdsEnd
        FROM refGene
        WHERE name2='{g}'
        """.format(g=gene)

        if tx and not cds:
            self.c.execute(txsql)
        elif cds and not tx:
            self.c.execute(cdssql)
        generegions = list()
        for i in self.c.fetchall():
            generegions.append([i[0], i[1], i[2]])
        return [ii for ii in generegions]


    def parse_bed_file(self, bed):
        genesout = list()
        bedname = os.path.splitext(bed)[0]
        with open(bed, 'r') as f, open('{}.annotated'.format(bedname), 'w') as fout:
            for line in f:
                chromosome, start, end = line.split()
                genename = self.get_genename(chromosome, int(start) + 26, int(end) - 25)
                fout.write('{}\t{}\t{}\t{}\n'.format(chromosome, start, end, genename))
                genesout.append(genename)
        if self.genes is not None:
            notfound = [gene for gene in self.genes if gene not in genesout]
            notrequested = [gene for gene in genesout if gene not in self.genes ]
            if len (notfound) > 0:
                notfound.sort()
                logging.info('Niet in BEDfile: {}'.format(' '.join(notfound)))
                print('Niet in BEDfile: {}'.format(' '.join(notfound)))
            if len (notrequested) > 0:
                notrequested.sort()
                logging.info('Niet in genlijst: {}'.format(' '.join(set(notrequested))))
                print('Niet in genlijst: {}'.format(' '.join(set(notrequested))))

class Targets(object):

    def __init__(self, test, bedfile=None):
        self.targetdir = os.path.abspath(os.path.dirname(__file__))
        self.db = os.path.join(self.targetdir, 'varia', 'capinfo.sqlite')
        self.test = test
        self.df = pd.read_sql('SELECT * FROM capdb WHERE (actief=1)',
                              con=sqlite3.connect(self.db))
        if self.df[self.df['genesiscode'] == self.test].empty:
            print ('Genesiscode voor test bestaat niet in database.')
            sys.exit()

        self.capture = self.get_capture()
        self.pakket = self.get_pakket()
        self.panel = self.get_panel()
        if bedfile is not None:
            self.bedfile = bedfile
            self.bed = self.parse_bed()
        elif bedfile is None:
            self.bedfile = None

    def get_capture(self):
        return ''.join(self.df[self.df['genesiscode'] == self.test]['capture'].values)

    def get_pakket(self):
        return ''.join(self.df[self.df['genesiscode'] == self.test]['pakket'].values)

    def get_panel(self):
        return ''.join(self.df[self.df['genesiscode'] == self.test]['panel'].values)

    def delversion(self, withversion):
        noversion = withversion.split('v')[0]
        return noversion

    def genelist(self, gf):
        with open(gf, 'r') as f:
            lines = (line.rstrip() for line in f)
            lines = list(line for line in lines if line)
        return [l.split()[0] for l in lines]

    def get_dir(self):
        if self.capture == self.pakket:
            return '{}/{}'.format(self.targetdir, self.delversion(self.capture))
        elif self.capture != self.pakket:
            return '{}/{}/{}'.format(self.targetdir, self.delversion(self.capture),
                                     self.delversion(self.pakket))

    def get_genes_from_file(self):
        return self.genelist('{}/{}_genes.txt'.format(self.get_dir(), self.pakket))

    def get_agenes_from_file(self):
        if self.panel == 'False':
            return self.get_genes_from_file()
        return self.genelist('{}/corepanels/{}_genes.txt'.format(self.get_dir(), self.panel))

    def get_cgenes_from_file(self):
        genes = self.get_genes_from_file()
        [genes.remove(i) for i in self.get_agenes_from_file()]
        return genes

    def get_size(self, df):
        size = pd.Series(df['end'] - df['start'])
        return size.sum()

    def update_gene_database(self):
        genes = self.get_genes_from_file()
        agenes = self.get_agenes_from_file()

        if self.panel == 'False':
            genes = json.dumps(genes)
            capsize = self.get_size(self.bed)
            pakketsize = self.get_size(agenes)
            sql ='''INSERT INTO genes
            (genesiscode, capture, pakket, panel, capturesize, pakketsize, genen)
            VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')
            '''.format(self.test, self.capture, self.pakket, self.panel,
            capsize, pakketsize, genes)

        elif self.panel != 'False':
            capsize = self.get_size(self.bed)
            pakketsize = self.get_size(self.filter_genes_from_df(genes))
            panelsize = self.get_size(self.filter_genes_from_df(agenes))
            genes = json.dumps(genes)
            agenes = json.dumps(agenes)

            if self.panel == 'OVRv1' or self.panel == 'BMUTtypeAv1':
                cgenes = genes
            else:
                cgenes = json.dumps(self.get_cgenes_from_file())
            sql = '''INSERT INTO genes
            (genesiscode, capture, pakket, panel, capturesize, pakketsize, panelsize, genen, agenen, cgenen)
            VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
            '''.format(self.test, self.capture, self.pakket, self.panel, capsize,
                       pakketsize, panelsize, genes, agenes, cgenes)
        print(sql)
        # c.execute(sql)

    def filter_genes_from_df(self, genelist):
        if self.bedfile is None:
            raise OSError('Geen BED file opgegeven')
        else:
            return self.bed[self.bed.gene.isin(genelist)]

    def parse_bed(self):
        bed = pd.read_csv(self.bedfile, sep='\t', header=None)
        bed.columns = ['chromosome', 'start', 'end', 'gene']
        return bed

    def write_bed(self, df, fout):
        df.to_csv(fout, index=False, header=False, sep='\t')

    def create_bed_for_pakket(self, genes):
        try:
            dfout = self.filter_genes_from_df(genes)
        except OSError as e:
            print(e)
        else:
            self.write_bed(dfout, '{}/{}_exonplus20.bed'.format(self.get_dir(),
                                                                self.pakket))
            print('{} {} Pakket bed created!'.format(date(), now()))

    def create_bed_for_panel(self, genes):
        try:
            dfout = self.filter_genes_from_df(genes)
        except OSError as e:
            print(e)
        else:
            self.write_bed(dfout, '{}/corepanels/{}.bed'.format(self.get_dir(),
                                                                self.panel))
            print('{} {} Panel bed created!'.format(date(), now()))

    def get_generegion(self, gene):
        return Annotation().get_region(gene)

    def create_bed_for_generegion(self):
        genebed = '{}/{}_generegions.bed'.format(self.get_dir(), self.pakket)
        with open(genebed, 'w') as fout:
            for g in self.get_genes_from_file():
                regions = self.get_generegion(g)
                for region in regions:
                    fout.write('{}\t{}\t{}\n'.format(region[0], region[1], region[2]))

    def create_files_for_test(self):
        if not self.capture == self.pakket:
            self.create_bed_for_pakket(self.get_genes_from_file())
        if self.panel != 'False' and self.panel != 'OVRv1':
            self.create_bed_for_panel(self.get_agenes_from_file())
        self.update_gene_database()


def get_arguments():
    """Parse arguments and return Namespace object."""

    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bed", type=str, metavar='',
                        help="BED file",  required=True)
    parser.add_argument("-g", "--genelist", type=str, metavar='',
                        help="File with gene names")
    parser.add_argument("-t", "--testcode", type=str, metavar='',
                        help="Genesiscode for test")
    parser.add_argument("-c", "--createfiles", action='store_true',
                        help="Create files for pakket and or panel")
    return parser.parse_args()

def now():
    return time.strftime('%H:%M:%S')

def date():
    return time.strftime('%d/%m/%Y')

def main():
    args = get_arguments()
    if args.bed:
        bed, extension = os.path.splitext(args.bed)
        if extension == '.bed':
            annotate(args)
            args.bed = '{}.annotated'.format(bed)
    if args.createfiles:
        if not args.testcode:
            print ('Geen genesiscode opgegeven.')
            sys.exit()
        if not args.bed:
            print ('Geen bedfile opgegeven.')
        print('{} {} Creating files'.format(date(), now()))
        Targets(args.testcode, args.bed).create_files_for_test()


def annotate(args):
    logging.basicConfig(filename='{}.annotation.log'.format(args.bed),
                        format='%(levelname)s:%(message)s',
                        level=logging.DEBUG,
                        filemode='w')
    logging.info('{} {} Annotating {} @ UCSC'.format(date(), now(), args.bed))
    print('{} {} Annotating {} @ UCSC'.format(date(), now(), args.bed))
    if args.genelist:
        Annotation(genefile=args.genelist).parse_bed_file(args.bed)
    elif not args.genelist:
        Annotation().parse_bed_file(args.bed)
    logging.info('{} {} Done.'.format(date(), now()))
    print('{} {} Done.'.format(date(), now()))

if __name__ == '__main__':
    main()
