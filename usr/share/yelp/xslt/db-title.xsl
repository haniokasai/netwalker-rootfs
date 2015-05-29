<?xml version='1.0' encoding='UTF-8'?><!-- -*- indent-tabs-mode: nil -*- -->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:yelp="http://www.gnome.org/yelp/ns"
                xmlns="http://www.w3.org/1999/xhtml"
                extension-element-prefixes="yelp"
                version="1.0">

<xsl:import href="/usr/share/xml/gnome/xslt/docbook/common/db-title.xsl"/>

<xsl:template name="node"/>

<xsl:output method="text"/>

<xsl:template match="/">
  <xsl:variable name="title">
    <xsl:call-template name="db.titleabbrev">
      <xsl:with-param name="node" select="$node"/>
    </xsl:call-template>
  </xsl:variable>
  <xsl:value-of select="normalize-space($title)"/>
</xsl:template>

</xsl:stylesheet>
