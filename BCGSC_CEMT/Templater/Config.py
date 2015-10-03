from collections import namedtuple
from MinimalPyUtils import *

class Parser:
	@staticmethod
	def antibody(arg):
		tags = map(lambda x: x.strip().lower(), arg.split())
		if tags[0] == 'histone': return arg.strip().split()[1]
		elif tags[0] == 'chip-seq' and tags[1] == 'input': return 'Input'
		else: raise Exception('?? ' + arg)

class Config:
	valid_assays = {}
	antibodies = ['H3K4me3', 'H3K9me3', 'H3K27me3', 'H3K4me1', 'H3K27ac', 'H3K36me3', 'Input', 'H3K9ac']
	chip_input = ['Input', 'input'] 
	wgbs = ['Bisulfite-Seq', 'WGBS', 'DNA Methylation', 'dna methylation', 'bisulfite-seq', 'wgbs']
	wgs = ['WGS', 'wgs']
	mirna = ['miRNA-Seq', 'smrna-seq', 'smRNA-Seq', 'mirna', 'miRNA-Seq']
	chip = antibodies + ['chip-seq', 'ChIP-Seq', ]
	rna = ['RNA-Seq']
	medip = ['MeDIP-Seq:Methylcytidine', 'MeDIP-Seq']
	medip_antibody = ['Methylcytidine']
	mreseq = ['MRE-Seq']
	assays = {
		"MeDIP-Seq:Methylcytidine" : "MeDIP-Seq",
		"Histone H3K9ac" : "H3K9ac",
		'Histone H3K4me1' : 'H3K4me1',
		'Histone H3K4me3' : 'H3K4me3', 
		'Histone H3K9me3' : 'H3K9me3', 
		'Histone H3K27me3' : 'H3K27me3', 
		'Histone H3K36me3' : 'H3K36me3', 
		'Histone H3K27ac' : 'H3K27ac', 
		'ChIP-Seq Input' : 'Input',
		'smRNA-Seq' : 'smRNA',
		'mRNA-Seq' : 'mRNA',  
		'DNA Methylation' : 'WGBS',
		'WGS' : 'WGS',
		"MeDIP-Seq": "MeDIP-Seq",
		"MRE-Seq": "MRE-Seq",
	}
	standardize_assays = {
		"MeDIP-Seq:Methylcytidine" : "MeDIP-Seq:Methylcytidine",
		"MeDIP-Seq": "MeDIP-Seq",
		"MRE-Seq": "MRE-Seq",
		"H3K9ac" : "Histone H3K9ac",
		"H3K27ac": "Histone H3K27ac",
		"H3K27me3": "Histone H3K27me3",
		"H3K36me3": "Histone H3K36me3",
		"H3K4me1": "Histone H3K4me1",
		"H3K4me3": "Histone H3K4me3",
		"H3K9me3": "Histone H3K9me3",
		"Input": "ChIP-Seq Input",
		"WGBS": "DNA Methylation",
		"Bisulfite-Seq" : "DNA Methylation",
		"WGS": "WGS",
		"smRNA": "smRNA-Seq",
		"RNA-Seq": "mRNA-Seq",
		"mRNA": "mRNA-Seq",
	}

	def __init__(self, settings):
		self.__settings__ = settings
		self.__view__ = settings['__view__']


	def view(self, experiment, track_type):
		if experiment in Config.antibodies:
			return { 
					'color' : self.__view__['chip']['color'][experiment],
					'maxHeightPixels' : self.__view__['chip']['maxHeightPixels'][track_type],
					'visibility' : self.__view__['chip']['visibility'][track_type],
					'filetype' : self.__view__['chip']['filetype'][track_type],
			}
		else:
			return self.__view__['except_chip'][experiment][track_type]
	










