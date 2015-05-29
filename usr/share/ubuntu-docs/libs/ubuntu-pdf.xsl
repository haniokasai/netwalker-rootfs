<?xml version="1.0" encoding="ISO-8859-1"?>
<!-- Customization layer for PDF output 
     License: CC-BY-SA. see http://creativecommons.org/licenses/by-sa/2.0/
-->

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
xmlns:fo="http://www.w3.org/1999/XSL/Format">

<!-- Import the new xsl -->
<xsl:import href="/usr/share/xml/docbook/stylesheet/nwalsh/fo/docbook.xsl"/>

<!-- ***************  Fonts  *********************  -->
<!-- ***************************************************  -->

<!-- Use a serif font -->
<xsl:param name="body.font.family" select="'serif'"/>
<xsl:param name="symbol.font.family" select="'Symbol'"/>
<xsl:param name="dingbat.font.family">
   <xsl:value-of select="$body.font.family"/>
</xsl:param>
<xsl:param name="title.font.family">
   <xsl:value-of select="$body.font.family"/>
</xsl:param>
<xsl:param name="body.font.master">11</xsl:param>
<xsl:param name="body.font.size">
 <xsl:value-of select="$body.font.master"/><xsl:text>pt</xsl:text>
</xsl:param>

<xsl:param name="monospace.font.family" select="'monospace'"></xsl:param>

<!-- Smaller monospace -->
<xsl:attribute-set name="monospace.properties">
  <xsl:attribute name="font-size">80%</xsl:attribute>
</xsl:attribute-set>

<xsl:param name="line-height" select="'1.5'"></xsl:param>

<!-- ***************  Page Format  *********************  -->
<!-- ***************************************************  -->

<!-- Define the page width/height -->
<xsl:param name="page.width">21cm</xsl:param>
<xsl:param name="page.height">29.7cm</xsl:param>

<!-- Give each section a number -->
<xsl:param name="section.autolabel" select="1"></xsl:param>

<!-- Turn on left justify. The default is full justify -->
<xsl:param name="alignment">left</xsl:param> 

<!-- Margins -->
<xsl:param name="page.margin.outer">
  <xsl:choose>
    <xsl:when test="$double.sided != 0">0.75in</xsl:when>
    <xsl:otherwise>1in</xsl:otherwise>
  </xsl:choose>
</xsl:param>
<xsl:param name="page.margin.inner">
  <xsl:choose>
    <xsl:when test="$double.sided != 0">1in</xsl:when>
    <xsl:otherwise>1in</xsl:otherwise>
  </xsl:choose>
</xsl:param>

<!-- Keep paragraphs flush with the left hand side -->
<xsl:param name="body.start.indent" select="'0pc'"/>
<xsl:param name="title.margin.left" select="'0pc'"/>

<!-- Put a rule above each footer and a rule below each header  -->
<xsl:param name="footer.rule" select="0"/>
<xsl:param name="header.rule" select="1"/>

<!-- Don't split words across lines (no end-of-line word breaks) -->
<xsl:param name="hyphenate">false</xsl:param>

<!-- '1 3 1' means the center header has three times the width of the left and 
     right headers. This is needed because the doc title is in the center header -->
<xsl:param name="header.column.widths" select="'1 3 1'"/>

<!-- ***************  Headers  *********************  -->
<!-- ***************************************************  -->

<xsl:attribute-set name="section.title.properties">
  <xsl:attribute name="font-family">
    <xsl:value-of select="$title.font.family"></xsl:value-of>
  </xsl:attribute>
  <xsl:attribute name="font-weight">normal</xsl:attribute>
  <!-- font size is calculated dynamically by section.heading template -->
  <xsl:attribute name="keep-with-next.within-column">always</xsl:attribute>
  <xsl:attribute name="space-before.minimum">0.8em</xsl:attribute>
  <xsl:attribute name="space-before.optimum">1.0em</xsl:attribute>
  <xsl:attribute name="space-before.maximum">1.2em</xsl:attribute>
  <xsl:attribute name="text-align">left</xsl:attribute>
  <xsl:attribute name="start-indent"><xsl:value-of select="$title.margin.left"></xsl:value-of></xsl:attribute>
</xsl:attribute-set>

<xsl:attribute-set name="section.title.level1.properties">
  <xsl:attribute name="font-weight">bold</xsl:attribute>
  <xsl:attribute name="text-decoration">underline</xsl:attribute>
  <xsl:attribute name="font-size">
    <xsl:value-of select="$body.font.master * 1.5"></xsl:value-of>
    <xsl:text>pt</xsl:text>
  </xsl:attribute>
  <xsl:attribute name="break-before">page</xsl:attribute>
</xsl:attribute-set>

<xsl:attribute-set name="section.title.level2.properties">
  <xsl:attribute name="text-decoration">underline</xsl:attribute>
  <xsl:attribute name="font-size">
    <xsl:value-of select="$body.font.master * 1.3"></xsl:value-of>
    <xsl:text>pt</xsl:text>
  </xsl:attribute>
</xsl:attribute-set>

<xsl:attribute-set name="section.title.level3.properties">
  <xsl:attribute name="text-decoration">underline</xsl:attribute>
  <xsl:attribute name="font-size">
    <xsl:value-of select="$body.font.master * 1"></xsl:value-of>
    <xsl:text>pt</xsl:text>
  </xsl:attribute>
</xsl:attribute-set>

<xsl:attribute-set name="section.title.level4.properties">
  <xsl:attribute name="font-style">italic</xsl:attribute>
  <xsl:attribute name="font-size">
    <xsl:value-of select="$body.font.master * 1"></xsl:value-of>
    <xsl:text>pt</xsl:text>
  </xsl:attribute>
</xsl:attribute-set>

<!-- ***************  Links  *********************  -->
<!-- ***************************************************  -->

<!-- urls in brackets for ulinks -->
<xsl:param name="ulink.show" select="1"></xsl:param>

<!-- ulink formatting -->
<xsl:attribute-set name="xref.properties">
  <xsl:attribute name="font-style">italic</xsl:attribute>
</xsl:attribute-set>

<xsl:param name="ulink.footnotes" select="'yes'"></xsl:param>
<xsl:attribute-set name="footnote.mark.properties">
  <xsl:attribute name="font-size">65%</xsl:attribute>
  <xsl:attribute name="font-weight">normal</xsl:attribute>
  <xsl:attribute name="font-style">normal</xsl:attribute>
</xsl:attribute-set>
<xsl:attribute-set name="footnote.properties">
  <xsl:attribute name="font-size">70%</xsl:attribute>
  <xsl:attribute name="font-weight">normal</xsl:attribute>
  <xsl:attribute name="font-style">normal</xsl:attribute>
</xsl:attribute-set>

<!-- page numbers included in xref cross references -->
<xsl:param name="insert.xref.page.number">yes</xsl:param>

<!-- This customises the page number format -->
<xsl:param name="local.l10n.xml" select="document('')"/>
<l:i18n xmlns:l="http://docbook.sourceforge.net/xmlns/l10n/1.0">
  <l:l10n language="en">
    <l:context name="xref">
      <l:template name="page.citation" text=" [p. %p]"/>
    </l:context>
  </l:l10n>
</l:i18n>

<!-- ***************  Admonitions  *********************  -->
<!-- ***************************************************  -->

<!-- If true (non-zero), admonitions are presented in an alternate style that uses a graphic. Default graphics are provided in the distribution. -->
<xsl:param name="admon.graphics" select="1"></xsl:param>

<!-- If true (non-zero), admonitions are presented with a generated text label such as Note or Warning in the appropriate language. If zero, such labels are turned off, but any title children of the admonition element are still output. The default value is 1. -->
<xsl:param name="admon.textlabel" select="0"></xsl:param>

<xsl:param name="admon.graphics.path" select="'libs/admon/'"/>
<xsl:param name="admon.graphics.extension" select="'.png'"/>

<xsl:template match="*" mode="admon.graphic.width">
  <xsl:text>24pt</xsl:text>
</xsl:template>

<!-- ***************  ToC/LoT/Index Generation  *********************  -->
<!-- ***************************************************  -->

<!-- Specifies the depth to which recursive sections should appear in the TOC -->
<xsl:param name="toc.section.depth" select="1" />

<!-- How maximaly deep should be each TOC? -->
<xsl:param name="toc.max.depth" select="2" />

<!-- **************** Miscellaneous Fixes ****************** -->
<!-- ***************************************************  -->

<!-- Some custom spacing for lists -->

<xsl:attribute-set name="list.block.spacing">
  <xsl:attribute name="space-before.optimum">0.3em</xsl:attribute>
  <xsl:attribute name="space-before.minimum">0.2em</xsl:attribute>
  <xsl:attribute name="space-before.maximum">0.5em</xsl:attribute>
  <xsl:attribute name="space-after.optimum">0.3em</xsl:attribute>
  <xsl:attribute name="space-after.minimum">0.2em</xsl:attribute>
  <xsl:attribute name="space-after.maximum">0.5em</xsl:attribute>
</xsl:attribute-set>

<xsl:attribute-set name="list.item.spacing">
  <xsl:attribute name="space-before.optimum">0.3em</xsl:attribute>
  <xsl:attribute name="space-before.minimum">0.2em</xsl:attribute>
  <xsl:attribute name="space-before.maximum">0.5em</xsl:attribute>
</xsl:attribute-set>

<xsl:param name="variablelist.as.blocks" select="1"></xsl:param>

<!-- Get rid of annoying white page after titlepage -->
<xsl:template name="book.titlepage.separator"/>

<xsl:param name="fop1.extensions" select="'yes'"/>
<xsl:param name="fop.extensions" select="'yes'"/>
<xsl:template match="*" mode="fop.outline"/> 

<!-- select draft mode, either yes or no -->
<xsl:param name="draft.mode" select="'no'"/>

</xsl:stylesheet>

