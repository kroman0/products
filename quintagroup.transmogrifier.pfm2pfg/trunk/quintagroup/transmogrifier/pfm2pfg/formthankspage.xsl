<xsl:stylesheet version="1.0" 
     xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
     xmlns:at="http://plone.org/ns/archetypes/"
     xmlns:cmf="http://cmf.zope.org/namespaces/default/"
     xmlns:dc="http://purl.org/dc/elements/1.1/">

<xsl:template match="/">
    <xsl:for-each select="*">
        <!-- matched 'metadata' element and we copy it -->
        <xsl:copy>
            <xsl:for-each select="*|text()">
                <xsl:choose>
                    <!-- do some special with 'field' elements -->
                    <xsl:when test="name()='field'">
                        <xsl:apply-templates select="." />
                    </xsl:when>
                    <!-- copy all other elements -->
                    <xsl:otherwise>
                        <xsl:copy-of select="."/>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:for-each>
        </xsl:copy>
    </xsl:for-each>
</xsl:template>

<xsl:template match="at:field">
    <xsl:choose>
        <xsl:when test="@name='sent_title'">
            <dc:title>
                <xsl:value-of select="."/>
            </dc:title>
        </xsl:when>
        <xsl:when test="@name='sent_message'">
            <xsl:copy>
                <xsl:attribute name="name">thanksPrologue</xsl:attribute>
                <xsl:value-of select="." />
            </xsl:copy>
        </xsl:when>
        <!-- skip all other elements -->
        <xsl:otherwise />
    </xsl:choose>
</xsl:template>

</xsl:stylesheet>
