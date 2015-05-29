<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <!-- This file is a customization layer for HTML only -->
    <!-- ======================= -->
    <!-- Imports -->
	<xsl:import href="/usr/share/xml/docbook/stylesheet/nwalsh/xhtml/docbook.xsl"/>

    <!-- Params -->
    <xsl:param name="generate.legalnotice.link" select="1"/>
	<!-- requires DocBook XSL 1.69.1a -->
    <xsl:param name="generate.revhistory.link" select="1"/>
    <xsl:param name="toc.max.depth" select="2"/>
    <xsl:param name="chunker.output.indent" select="'yes'"/>
    <xsl:param name="body.font.master" select="10"/>
    <xsl:param name="html.stylesheet" select="'../../libs/ubuntu-book.css'"/>
    <xsl:param name="shade.verbatim" select="0"/>
    <xsl:param name="draft.mode" select="'no'"/>

	<!--Navigation Graphics-->
	<xsl:param name="navig.graphics" select="1"/>
	<xsl:param name="navig.graphics.path" select="'../../navig/'"/>
	<xsl:param name="navig.graphics.extension" select="'.png'"/> 
	<xsl:param name="navig.showtitles" select="1"/>
	
	<!--Admon Graphics--> 
	<xsl:param name="admon.graphics" select="1"/>
	<xsl:param name="admon.textlabel" select="0"/>
	<xsl:param name="admon.graphics.path" select="'../../admon/'"/>
	<xsl:param name="admon.graphics.extension" select="'.png'"/>
	
	<!-- Callout Graphics -->
	<xsl:param name="callout.unicode" select="1"/>
	<xsl:param name="callout.graphics" select="0"/>
	<xsl:param name="callout.graphics.path" select="'../../callouts/'"/>
	<xsl:param name="callout.graphics.extension" select="'.png'"/>
	
    <!-- Inline Formatting -->
    <xsl:template match="application">
      <xsl:call-template name="inline.boldseq"/>
    </xsl:template>
    <xsl:template match="guibutton">
      <xsl:call-template name="inline.boldseq"/>
    </xsl:template>
    <xsl:template match="guilabel">
      <xsl:call-template name="inline.italicseq"/>
    </xsl:template>
    
	<!-- this strippath template is copied from the 1.68.1 version of common.xls  -->
	<xsl:template name="strippath">
	  <xsl:param name="filename" select="''"/>
	  <xsl:choose>
	    <!-- Leading .. are not eliminated -->
	    <xsl:when test="starts-with($filename, '../')">
	      <xsl:value-of select="'../'"/>
	      <xsl:call-template name="strippath">
	        <xsl:with-param name="filename" select="substring-after($filename, '../')"/>
	      </xsl:call-template>
	    </xsl:when>
	    <xsl:when test="contains($filename, '/../')">
	      <xsl:call-template name="strippath">
	        <xsl:with-param name="filename">
	          <xsl:call-template name="getdir">
	            <xsl:with-param name="filename" select="substring-before($filename, '/../')"/>
	          </xsl:call-template>
	          <xsl:value-of select="substring-after($filename, '/../')"/>
	        </xsl:with-param>
	      </xsl:call-template>
	    </xsl:when>
	    <xsl:otherwise>
	      <xsl:value-of select="$filename"/>
	    </xsl:otherwise>
	  </xsl:choose>
	</xsl:template>

</xsl:stylesheet>
