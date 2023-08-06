#!/usr/bin/python2.7
import os, egglib, sys, unittest, random, re, resource, gc, time
sys.settrace


def show_site(site):
    print '----------------------------------------------------------------'
    print '# -> ns:          ', site.ns
    print '# -> ingroup:     ', site.num_ingroup
    print '# -> alleles:     ', site.alleles(), map(chr, site.alleles())
    print '----------------------------------------------------------------'
    """
    print '# -> no:          ', site.no

    print '# -> outgroup:    ', site.num_outgroup
    print '# -> missing:     ', site.num_missing
    print '# -> in ingroup:  ', site.num_missing_ingroup
    print '# -> in outgroup: ', site.num_missing_outgroup
    print '# -> num all:     ', site.num_alleles
    print '# -> ploidy:      ', site.ploidy
    print '# -> alleles:     ', site.alleles(), map(chr, site.alleles())
    print '# -> default:     ', site.as_list()
    print '# -> flat:        ', site.as_list(flat=True)
    print '# -> ingroup:     ', site.as_list(skip_outgroup=True)
    """

if __name__ == "__main__":



   vcf_file="human_fragment.vcf"
   idx_file="human_fragment.vcfi"
   bed_file="human_fragment.bed"

   vcf=egglib.io.VcfParser(vcf_file, allow_X=True , allow_gap=True, find_index=False)
   ##vcf.make_index()
   
   vcf.get_bed_file(bed_file)
   bsw = vcf.bed_slider(100,2)


   for i in xrange(vcf._bed.n_bed_data()):
	print "{0}\t{1}".format(vcf._bed.get_bed_data(i).start_pos, vcf._bed.get_bed_data(i).end_pos)

   while bsw.good:
       bsw.next()


   """
   CS = egglib.stats.ComputeStats()
   CS.add_stats('D')

   while bsw.good:
       bsw.next()
       print bsw.num_sites
       show_site(bsw[10])
       print CS.process_sites(bsw)

	#show_site(bsw[10])
   #merged_filt_depth_75_200_ssduplicateindANDsnp-ssblanck_DEF_for_structure
   #vcf=egglib.io.VcfParser('merged_filt_depth_75_200_ssduplicateindANDsnp-ssblanck_DEF_for_structure.vcf', allow_X=False , allow_gap=True) PROBLEME POUR LES STATS

   print "///////////////////////////////////////////////////"
   vcf.rewind()
   wdw=vcf.slider(100,50,0,2)
	

   while wdw.good:
       wdw.next()
       print wdw.num_sites
       show_site(wdw[10])
       print CS.process_sites(wdw)


   vcf.rewind()

   bsw.at(0)
   show_site(bsw[0])
   show_site(bsw[1])
   show_site(bsw[2])
   show_site(bsw[3])
   show_site(bsw[4])
   """




































   """

   path_vcf="data_vcf/"
   path_vcfi="data_vcfi/"

   l_vcf=['LG01.vcf','LG02.vcf','LG03.vcf','LG04.vcf','LG05.vcf','LG06.vcf','LG07.vcf','LG08.vcf','LG09.vcf','LG10.vcf','LG11.vcf','LG12.vcf','LG13.vcf','LG14.vcf','LG15.vcf','LG16.vcf', 'LG17.vcf', 'LG18.vcf']
   for vcf in l_vcf:
      vcf=egglib.io.VcfParser(path_vcf+vcf, allow_X=True , allow_gap=True)
      vcf.make_index()




   print vcf.get_index()
   #vcf.goto('3', 9719386)
   #vcf.goto('1')
   print vcf.get_index()

   wdw=vcf.slider(50,50,0,2, fill=True, start_pv=0, end_pv=50)
   CS = egglib.stats.ComputeStats()
   CS.add_stats('R', 'He')

   while(wdw.good):
      wdw.next()
      print CS.process_sites(wdw)

   """
  
