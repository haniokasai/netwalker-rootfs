<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  version="1.0">

<!-- This modification looks a bit large but is a couple of lines change to make the draft watermark appear in the #content div wrapper rather than the body background -->

<xsl:template name="head.content">
  <xsl:param name="node" select="."/>
  <xsl:param name="title">
    <xsl:apply-templates select="$node" mode="object.title.markup.textonly"/>
  </xsl:param>

  <title>
    <xsl:copy-of select="$title"/>
  </title>

  <xsl:if test="$html.stylesheet != ''">
    <xsl:call-template name="output.html.stylesheets">
      <xsl:with-param name="stylesheets" select="normalize-space($html.stylesheet)"/>
    </xsl:call-template>
  </xsl:if>

  <xsl:if test="$link.mailto.url != ''">
    <link rev="made" href="{$link.mailto.url}"/>
  </xsl:if>

  <xsl:if test="$html.base != ''">
    <base href="{$html.base}"/>
  </xsl:if>

<!--  <meta name="generator" content="DocBook {$DistroTitle} V{$VERSION}"/> -->

  <xsl:if test="$generate.meta.abstract != 0">
    <xsl:variable name="info" select="(articleinfo                                       |bookinfo                                       |prefaceinfo                                       |chapterinfo                                       |appendixinfo                                       |sectioninfo                                       |sect1info                                       |sect2info                                       |sect3info                                       |sect4info                                       |sect5info                                       |referenceinfo                                       |refentryinfo                                       |partinfo                                       |info                                       |docinfo)[1]"/>
    <xsl:if test="$info and $info/abstract">
      <meta name="description">
        <xsl:attribute name="content">
          <xsl:for-each select="$info/abstract[1]/*">
            <xsl:value-of select="normalize-space(.)"/>
            <xsl:if test="position() &lt; last()">
              <xsl:text> </xsl:text>
            </xsl:if>
          </xsl:for-each>
        </xsl:attribute>
      </meta>
    </xsl:if>
  </xsl:if>

  <xsl:if test="($draft.mode = 'yes' or                 ($draft.mode = 'maybe' and                 ancestor-or-self::*[@status][1]/@status = 'draft'))                 and $draft.watermark.image != ''">
    <style type="text/css"><xsl:text>
#content { background-image: url('</xsl:text>
<xsl:value-of select="$draft.watermark.image"/><xsl:text>');
       background-repeat: repeat-y;
       background-position: top center;
       /* The following properties make the watermark "fixed" on the page. */
       /* I think that's just a bit too distracting for the reader... */
       /* background-attachment: fixed; */
       /* background-position: center center; */
     }</xsl:text>
    </style>
  </xsl:if>
  <xsl:apply-templates select="." mode="head.keywords.content"/>
</xsl:template>


</xsl:stylesheet>
