<xsl:stylesheet version="1.0" 
     xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
     xmlns:at="http://plone.org/ns/archetypes/"
     xmlns:cmf="http://cmf.zope.org/namespaces/default/">

<xsl:template match="/">
    <xsl:for-each select="*">
        <!-- matched 'metadata' element and we copy it -->
        <xsl:copy select=".">
            <xsl:for-each select="*|text()">
                <xsl:choose>
                    <!-- do some special with 'field' elements -->
                    <xsl:when test="name()='field'">
                        <xsl:apply-templates select="." />
                    </xsl:when>
                    <!-- change value of 'cmf:type' attribute -->
                    <xsl:when test="name()='cmf:type'">
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
        <!-- next fields are omitted -->
        <xsl:when test="@name='displayMode'" />
        <xsl:when test="@name='displayItems'" />
        <xsl:when test="@name='categories'" />
        <xsl:when test="@name='allowTrackback'" />
        <xsl:when test="@name='adminEmail'" />
        <!-- copy all other elements -->
        <xsl:otherwise>
            <xsl:copy-of select="."/>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

<xsl:template match="cmf:type">
    <xsl:copy select=".">
        <xsl:text>Weblog</xsl:text>
    </xsl:copy>
</xsl:template>

</xsl:stylesheet>
