# -*- coding: utf-8 -*-
import os
import time
import argparse
import gffutils
import pandas as pd
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from extract_UTR import utr
from extract_uORF import get_uorf
from extract_dORF import get_dorf
from extract_CDS import get_cds
from extract_promoter import get_promoter

def create(args):
    '''
    parameters:
     args: arguments from argparse
    '''
    fn = args.gff
    db = gffutils.create_db(fn, dbfn='gff.db', force=True, keep_order=True,\
        disable_infer_genes=True, disable_infer_transcripts=True,\
        merge_strategy='merge', sort_attribute_values=True)
    return db

def genome_dict(genome_fasta_path):
    '''
    parameters:
     genome_fasta_path: genome reference of organism
    return:
     genome fasta dict
    '''
    genome = dict()
    for record in SeqIO.parse(genome_fasta_path, 'fasta'):
        genome[record.id] = record.seq
    return genome


def UTR(args):
    '''
    parameters:
     args: arguments from argparse 
    '''
    db = gffutils.FeatureDB('gff.db', keep_order=True)
    if args.transcript:
        utr(db, args.genome, args.transcript, args.output)
    else:
        utr(db, args.genome, None, args.output)


def uORF(args):
    '''
    parameters:
     args: arguments from argparse
    '''
    db = gffutils.FeatureDB('gff.db', keep_order=True)
    if args.transcript:
        get_uorf(db, args.genome, args.transcript, args.output)
    else:
        get_uorf(db, args.genome, None, args.output)
        
        
def CDS(args):
    '''
    parameters:
     args: arguments from argparse
    '''
    db = gffutils.FeatureDB('gff.db', keep_order=True)
    if args.transcript:
        get_cds(args, db, args.genome, args.transcript, args.output)
    else:
        get_cds(args, db, args.genome, None)


def dORF(args):
    '''
    parameters:
     args: arugmensts from argparse
    '''
    db = gffutils.FeatureDB('gff.db', keep_order=True)
    if args.transcript:
        get_dorf(db, args.genome, args.transcript, args.output)
    else:
        get_dorf(db, args.genome, None, args.output)


def exon(args):
    '''
    parameters:
     args: arguments from argparse
    '''
    # parse arguments
    tr_id = args.transcript
    pass 


def promoter(args):
    '''
    parameters:
     args: arguments from argparse
    '''
    genomeDict = genome_dict(args.genome)
    db = gffutils.FeatureDB('gff.db', keep_order=True)
    if args.gene:
        get_promoter(args, db, genomeDict, args.genome, args.gene, args.length, args.utr_head, args.output)
    else:
        get_promoter(args, db, genomeDict, args.genome, None, args.length, args.utr_head, args.output)


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help='sub-command help')
# create subcommand 
parser_create = subparsers.add_parser('create', help='create annotation database')
parser_create.add_argument('-g', '--gff', type=str, help='genome annotation file')
parser_create.set_defaults(func=create)
# promoter subcommand
parser_promoter = subparsers.add_parser('promoter', help='extract promoter in genome or gene')
parser_promoter.add_argument('-g', '--gene', type=str, help='specific gene; if not given, return whole genes')
parser_promoter.add_argument('-l', '--length', type=int, help='promoter length before TSS')
parser_promoter.add_argument('-u', '--utr_head', type=int, help='utr5 length after TSS')
parser_promoter.add_argument('-f', '--genome', type=str, help='genome fasta')
parser_promoter.add_argument('-o', '--output', type=str, help = 'output csv file path')
parser_promoter.add_argument('-p', '--print', action="store_true", help='stdin')
parser_promoter.add_argument('-v', '--version', help = 'promoterExtract version', action = "store_true")
parser_promoter.set_defaults(func=promoter)

# UTR subcommand
parser_utr = subparsers.add_parser('UTR', help='extract untranslated region sequence in genome or gene')
parser_utr.add_argument('-f', '--genome', type=str, help='genome fasta file')
parser_utr.add_argument('-t', '--transcript', type=str, help='specific transcript id; if not given, \
                       whole transcript will return')
parser_utr.add_argument('-o', '--output', type=str, help='output file path')
parser_utr.set_defaults(func=UTR)

# uORF subcommand
parser_uORF = subparsers.add_parser('uORF', help='extract upper stream open reading sequence in genome or gene')
parser_uORF.add_argument('-f', '--genome', type=str, help='genome fasta')
parser_uORF.add_argument('-t', '--transcript', type=str, help='specific transcript id; if not given, \
                       whole transcript will return')
parser_uORF.add_argument('-o', '--output', type=str, help='output file path')
parser_uORF.set_defaults(func=uORF)

# CDS subcommand
parser_cds = subparsers.add_parser('CDS', help='extract coding sequence in genome or gene')
parser_cds.add_argument('-f', '--genome', type=str, help='genome fasta')
parser_cds.add_argument('-t', '--transcript', type=str, help='specific transcript id; if not given, \
                       whole transcript will return')
parser_cds.add_argument('-o', '--output', type=str, help='output file path')
parser_cds.add_argument('-p', '--print', action="store_true", help='stdin')
parser_cds.set_defaults(func=CDS)

# dORF subcommand 
parser_dORF = subparsers.add_parser('dORF', help='extract down stream open reading frame sequence in a genome or gene')
parser_dORF.add_argument('-f', '--genome', type=str, help='genome fasta')
parser_dORF.add_argument('-t', '--transcript', type=str, help='specific transcript id; if not given, \
                       whole transcript will return')
parser_dORF.add_argument('-o', '--output', type=str, help='output file path')
parser_dORF.add_argument('-p', '--print', action="store_true", help='stdin')
parser_dORF.set_defaults(func=dORF)

args = parser.parse_args()
print('[%s runing ...]'%(time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())))
args.func(args)
print('[%s finished ...]'%(time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())))



'''
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--length', type=int, help='promoter length before TSS')
    parser.add_argument('-u', '--utr_head', type=int, help='length after TSS')
    parser.add_argument('-f', '--genome', type=str, help='genome fasta')
    parser.add_argument('-g', '--gff', type=str, help='genome annotation file')
    parser.add_argument('-o', '--outdir', type=str, help='output directory')
    args = parser.parse_args()
    get_promoter(args.length, args.utr_head, args.genome, args.gff, args.outdir)
'''                                             
