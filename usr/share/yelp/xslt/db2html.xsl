<?xml version='1.0' encoding='UTF-8'?><!-- -*- indent-tabs-mode: nil -*- -->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:yelp="http://www.gnome.org/yelp/ns"
                xmlns="http://www.w3.org/1999/xhtml"
                extension-element-prefixes="yelp"
                version="1.0">

<xsl:import href="/usr/share/xml/gnome/xslt/docbook/html/db2xhtml.xsl"/>

<xsl:include href="yelp-common.xsl"/>

<xsl:param name="yelp.javascript"/>


<xsl:param name="db.chunk.chunk_top" select="true()"/>
<xsl:param name="db.chunk.extension" select="''"/>
<xsl:param name="db.chunk.info_basename"  select="'__yelp_info'"/>

<xsl:param name="db2html.navbar.top" select="false()"/>

<!-- == db.number == -->
<!--
FIXME: yelp:cache no longer works
<xsl:template name="db.number">
  <xsl:param name="node" select="."/>
  <yelp:cache key="db.number" node="$node">
    <xsl:apply-templates mode="db.number.mode" select="$node"/>
  </yelp:cache>
</xsl:template>
-->

<!-- == db.chunk == -->
<xsl:template name="db.chunk">
  <xsl:param name="node" select="."/>
  <xsl:param name="info"/>
  <xsl:param name="template"/>
  <xsl:param name="href">
    <xsl:choose>
      <xsl:when test="$template = 'info'">
        <xsl:value-of select="$db.chunk.info_basename"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="$node/@id"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:param>
  <xsl:param name="depth_of_chunk">
    <xsl:call-template name="db.chunk.depth-of-chunk">
      <xsl:with-param name="node" select="$node"/>
    </xsl:call-template>
  </xsl:param>
  <yelp:document href="{$href}">
    <xsl:call-template name="db.chunk.content">
      <xsl:with-param name="node" select="$node"/>
      <xsl:with-param name="info" select="$info"/>
      <xsl:with-param name="template" select="$template"/>
      <xsl:with-param name="depth_of_chunk" select="$depth_of_chunk"/>
    </xsl:call-template>
  </yelp:document>
  <xsl:if test="string($template) = ''">
    <xsl:call-template name="db.chunk.children">
      <xsl:with-param name="node" select="$node"/>
      <xsl:with-param name="depth_of_chunk" select="$depth_of_chunk"/>
    </xsl:call-template>
  </xsl:if>
</xsl:template>

<!-- == db.xref.target == -->
<xsl:template name="db.xref.target">
  <xsl:param name="linkend"/>
  <xsl:value-of select="concat('#', $linkend)"/>
</xsl:template>

<!-- == db2html.css.custom == -->
<xsl:template name="db2html.css.custom">
  <xsl:call-template name="yelp.common.css"/>
</xsl:template>

<!-- == db2html.division.head.extra == -->
<xsl:template name="db2html.division.head.extra">
  <script type="text/javascript">
    <xsl:attribute name="src">
      <xsl:value-of select="concat('file://', $yelp.javascript)"/>
    </xsl:attribute>
  </script>
</xsl:template>

</xsl:stylesheet>
