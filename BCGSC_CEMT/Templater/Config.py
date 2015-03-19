from collections import namedtuple
from PyUtils import *

class Parser:
	@staticmethod
	def antibody(arg):
		tags = map(lambda x: x.strip().lower(), arg.split())
		if tags[0] == 'histone': return arg.strip().split()[1]
		elif tags[0] == 'chip-seq' and tags[1] == 'input': return 'Input'
		else: raise Exception('?? ' + arg)

class Config:
	antibodies = ['H3K4me3', 'H3K9me3', 'H3K27me3', 'H3K4me1', 'H3K27ac', 'H3K36me3', 'Input']
	wgbs = ['Bisulfite-Seq', 'WGBS', 'DNA Methylation', 'dna methylation', 'bisulfite-seq', 'wgbs']
	wgs = ['WGS', 'wgs']
	mirna = ['miRNA-Seq', 'smrna-seq', 'smRNA-Seq', 'mirna', 'miRNA-Seq']
	chip = antibodies + ['chip-seq', 'ChIP-Seq', ]
	rna = ['RNA-Seq']
	assays = {
		'Histone H3K4me1' : 'H3K4me1',
		'Histone H3K4me3' : 'H3K4me3', 
		'Histone H3K9me3' : 'H3K9me3', 
		'Histone H3K27me3' : 'H3K27me3', 
		'Histone H3K36me3' : 'H3K36me3', 
		'Histone H3K27ac' : 'H3K27ac', 
		'ChIP-Seq Input' : 'Input',
		'smRNA-Seq' : 'miRNA',
		'mRNA-Seq' : 'ssRNA',  
		'DNA Methylation' : 'WGBS',
		'WGS' : 'WGS',
	}

	@staticmethod
	def View(experiment, track_type):
		if experiment in Config.antibodies:
			return { 
					'color' : Config.__View__['chip']['color'][experiment],
					'maxHeightPixels' : Config.__View__['chip']['maxHeightPixels'][track_type],
					'visibility' : Config.__View__['chip']['visibility'][track_type],
					'filetype' : Config.__View__['chip']['filetype'][track_type],
			}
		else:
			return Config.__View__['except_chip'][experiment][track_type]
	
	__View__ = {
		'chip' : {'color' : {
							 'H3K4me3' :'255,0,0',
							 'H3K4me1' : '255,102,51',
							 'H3K9me3' : '0,0,102',
							 'H3K36me3': '153,0,153',
							 'H3K27me3': '102,51,0',
							 'H3K27ac' : '51,102,255',
							 'Input'   : '0,0,0',
						},
					'visibility' : { 'thresholded' : 'full', 'normalized_signal' : 'full', 'signal' : 'full' },
					'maxHeightPixels' : {  'thresholded' : '10:10:10', 'normalized_signal' : '70:70:32', 'signal' : '70:70:32'},
					'filetype' : {  'thresholded' : 'bigWig', 'normalized_signal' : 'bigWig',  'signal' : 'bigWig'}, },

		'except_chip':  {
			'ssRNA' : {
				'rpkm_positive_strand': { 'color' : '180,30,100' , 'visibility' : 'dense', 'filetype' : 'bigWig', 'maxHeightPixels': '70:70:32' },
				'rpkm_negative_strand': { 'color' : '180,30,100' , 'visibility' : 'dense', 'filetype' : 'bigWig', 'maxHeightPixels': '70:70:32' },
			},
			'WGBS' : {
				'cpg_coverage': { 'color' : '100,100,100' , 'visibility' : 'dense', 'filetype' : 'bigWig', 'maxHeightPixels': '70:70:32' },
				'fractional_methylation_calls' : { 'color' : '0,250,100' , 'visibility' : 'dense', 'filetype' : 'bigWig', 'maxHeightPixels': '70:70:32' },
			},
			'WGS' : {
				'copy_number_variation': { 'color' : '153,0,153' , 'visibility' : 'dense', 'filetype' : 'bigWig', 'maxHeightPixels': '70:70:32' },
			},
			'miRNA' : {
				'miRNA_mapped_per_million': { 'color' : '0,0,102' , 'visibility' : 'dense', 'filetype' : 'bigWig', 'maxHeightPixels': '70:70:32' },
				'isoform_details': { 'color' : '255,0,0' , 'visibility' : 'dense', 'filetype' : 'bigBed 9', 'maxHeightPixels': '70:70:32'},
			}
		}
	}










