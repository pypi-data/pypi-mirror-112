import os, egglib, sys, unittest, random, re, gc, time
from collections import Iterable

"""
my_file= open("positions.txt", "r")
lines  = my_file.readlines()

total=0
end_i=0
lines_selected=[]
for line in lines:
	start, end = line.split("..")
	if (end_i<int(start)):
		lines_selected.append(line)
		total += (int(end)-int(start))+1
	else:
		pass
	end_i=int(end)
	#print int(start)
#print ','.join(lines_selected)
#for i in lines_selected:
#	print i
print total
my_file.close
"""

position_MtChr2=("3644..5878,5950..5958,6182..6221,7110..7501,11376..11978,12092..12169,12561..12804,"
		"13200..13290,13753..13891,14477..14899,14987..15184,16128..16239,16346..16458,18831..18931,"
		"19048..19108,19221..19493,19881..19943,20032..20131,20443..20525,21480..21533,22105..22182,"
				"22276..22332,22407..22622,23909..24046,24214..24384,24917..25129,25566..26114,26840..26983,"
				"38765..39166,39230..39696,39903..40111,40332..40894,40955..41281,49014..49415,49513..49581,"
				"49668..50276,50445..50627,50722..50781,50882..51085,51246..51494,51710..51808,52984..53178,"
				"53552..53644,53752..54018,54215..54433,57408..57544,57959..57986,60428..61024,61175..61257,"
				"62081..62445,62872..62998,70784..70795,71844..72154,72647..72743,72826..72903,73553..74269,"
				"75534..75899,77481..78245,78305..78451,79456..79659,79770..80000,83525..83683,85767..86033,"
				"86109..86216,86314..86866,86961..87350,88883..88899,89974..90135,90383..90461,90651..90775,"
				"92092..92424,94554..94627,94699..94762,95107..95254,95459..95577,96925..97192,97270..97706,"
				"98016..98132,98231..98527"
				)



def total_pb_position(positions):
	"""
        Method which calcul the number of bases covered by all position .

        :param positions: a string whicht contains all the positions
        
        """

	
	total=1
	list_pos=[]
	list_pos=positions.split(',')
	for i in list_pos:
		start,end=i.split('..')
		total += (int(end)-int(start))+1
	return total


total_=total_pb_position(position_MtChr2)
