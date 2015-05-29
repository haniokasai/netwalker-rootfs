<?xml version="1.0" encoding="ISO-8859-1"?>
<!-- Customization layer for PDF output 
     CREATION INFO:
        Author: Jeff Schering
        Date: April 23, 2005
        Version: 0.1
     REVISION INFO:
        Author: Jeff Schering 
        Date: January 3, 2006 
        Version: 0.2
        Description: added draft mode parameters
     REVISION INFO:
        Author: 
        Date: 
        Version: 0.3
        
     License: CC-BY-SA. see http://creativecommons.org/licenses/by-sa/2.0/
-->
<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
xmlns:fo="http://www.w3.org/1999/XSL/Format">

<!-- Import the standard xsl -->
<xsl:import href="/usr/share/xml/docbook/stylesheet/nwalsh/fo/docbook.xsl"/>

<!-- PARAMETERS SECTION -->

<!-- select draft mode, either yes or no -->
<xsl:param name="draft.mode" select="'no'"/>

<!-- if draft mode is on, then use ubuntu draft image. -->
<xsl:param name="draft.watermark.image" select="'https://wiki.ubuntu.com/htdocs/ubuntu/img/u-draft.png'"/>

<!-- Give each section a number -->
<xsl:param name="section.autolabel" select="0"></xsl:param>

<!-- Turn on left justify. The default is full justify  -->
<xsl:param name="alignment">left</xsl:param>

<!-- Create bookmarks in the PDF file 
     NOTE: this is only applicable if Apache fop is used -->
<xsl:param name="fop.extensions" select="1"/>

<!-- Put a rule above each footer and a rule below each header  -->
<xsl:param name="footer.rule" select="1"/>
<xsl:param name="header.rule" select="1"/>

<!-- Use a sans-serif font -->
<xsl:param name="body.font.family" select="'sans-serif'"/>

<!-- Don't split words across lines (no end-of-line word breaks) -->
<xsl:param name="hyphenate">false</xsl:param>

<!-- Don't make a table of contents -->
<xsl:param name="generate.toc">article nop</xsl:param>

<!-- '1 3 1' means the center header has three times the width of the left and 
     right headers. This is needed because the doc title is in the center header -->
<xsl:param name="header.column.widths" select="'1 3 1'"/>

<!-- TEMPLATE OVERRIDES SECTION -->

<!-- modify footer.content template from fo/pagesetup.xsl to change page number
     location from center to right -->
<xsl:template name="footer.content">
  <xsl:param name="pageclass" select="''"/>
  <xsl:param name="sequence" select="''"/>
  <xsl:param name="position" select="''"/>
  <xsl:param name="gentext-key" select="''"/>

  <fo:block>
    <!-- pageclass can be front, body, back -->
    <!-- sequence can be odd, even, first, blank -->
    <!-- position can be left, center, right -->
    <xsl:choose>
      <xsl:when test="$pageclass = 'titlepage'">
        <!-- nop; no footer on title pages -->
      </xsl:when>

      <xsl:when test="$double.sided != 0 and $sequence = 'even'
                      and $position='left'">
        <fo:page-number/>
      </xsl:when>

      <xsl:when test="$double.sided != 0 and ($sequence = 'odd' or $sequence = 'first')
                      and $position='right'">
        <fo:page-number/>
      </xsl:when>

<!-- This is the original
      <xsl:when test="$double.sided = 0 and $position='center'">
        <fo:page-number/>
      </xsl:when>
-->
     <!-- change from center to right -->
      <xsl:when test="$double.sided = 0 and $position='right'">
        <fo:page-number/>
      </xsl:when>


      <xsl:when test="$sequence='blank'">
        <xsl:choose>
          <xsl:when test="$double.sided != 0 and $position = 'left'">
            <fo:page-number/>
          </xsl:when>
          <xsl:when test="$double.sided = 0 and $position = 'center'">
            <fo:page-number/>
          </xsl:when>
          <xsl:otherwise>
            <!-- nop -->
          </xsl:otherwise>
        </xsl:choose>
      </xsl:when>


      <xsl:otherwise>
        <!-- nop -->
      </xsl:otherwise>
    </xsl:choose>
  </fo:block>
</xsl:template>


</xsl:stylesheet>
