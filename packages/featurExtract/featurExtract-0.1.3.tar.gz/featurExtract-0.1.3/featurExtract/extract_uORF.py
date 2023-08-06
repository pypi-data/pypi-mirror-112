# -*- coding: utf-8 -*-
import sys
import pandas as pd 
from collections import defaultdict

['TranscriptID','Chrom', 'Strand','CDS Interval','uORF Start','uORF End','uORF Type','uORF Length','uORF']

def uorf(transcript_id, chrom, strand, matural_transcript, coding_sequence):
    '''
    parameters:
     transcript_id:      transcript id
     matural_transcript: a Seq type (Biopython) from mature transcript without intron
     coding_sequence:    a Seq type (Biopython) from coding sequence start with ATG , 
                         end with TAA, TGA, TAG
    return:
     upper stream open reading frame
    '''
    uORF_dict = defaultdict(list)
    stop_codon_list = ['TAA','TAG','TGA']
    # start_codon means the first base position in matural_transcript
    start_codon = matural_transcript.index(coding_sequence)
    # stop_codon means the last base position in matural transcript
    cds_len = len(coding_sequence)
    stop_codon = start_codon + cds_len
    cds_intervel = str(start_codon) + '-' + str(stop_codon)
    mt_len = len(matural_transcript)
    utr5 = matural_transcript[:start_codon]
    utr5_len = len(utr5)
    utr3 = matural_transcript[stop_codon:]
    for i in range(0, utr5_len-3):
        # start codon find 
        if matural_transcript[i:i+3] == "ATG":
            for j in range(i+3,stop_codon,3):
            # stop codon find
                if matural_transcript[j:j+3] in stop_codon_list and j < utr5_len:
                    # type1 uORF  upstream; not unique 
                    type1_uORF = matural_transcript[i:j+3]
                    out1 = [transcript_id, chrom, strand, cds_intervel, i+1, j+3, 'type1', len(type1_uORF), type1_uORF]
                    if not uORF_dict.get('type1_uORF'):
                        uORF_dict['type1_uORF'] = [out1]
                    else:
                        uORF_dict['type1_uORF'].append(out1)
                    break 
                if matural_transcript[j:j+3] in stop_codon_list and j + 3 > utr5_len and j + 3 < stop_codon:
                    # type2 uORF across; the overlap region is triple or not; not unique
                    type2_uORF = matural_transcript[i:j+3]
                    out2 = [transcript_id, chrom, strand, cds_intervel, i+1, j+3, 'type2', len(type2_uORF), type2_uORF]
                    if not uORF_dict.get('type2_uORF'):
                        uORF_dict['type2_uORF'] = [out2]
                    else:
                        uORF_dict['type2_uORF'].append(out2)
                    break 
                if matural_transcript[j:j+3] in stop_codon_list and j + 3 > utr5_len and j+3 == stop_codon and (utr5_len - i)%3 == 0:
                    # N extention 通读; not unique 
                    type3_uORF = matural_transcript[i:utr5_len+cds_len]
                    out3 = [transcript_id, chrom, strand, cds_intervel, i+1, j+3, 'type3', len(type3_uORF), type3_uORF]
                    if not uORF_dict.get('type3_uORF'):
                        uORF_dict['type3_uORF'] = [out3]
                    else:
                        uORF_dict['type3_uORF'].append(out3)
                    break
    return uORF_dict

