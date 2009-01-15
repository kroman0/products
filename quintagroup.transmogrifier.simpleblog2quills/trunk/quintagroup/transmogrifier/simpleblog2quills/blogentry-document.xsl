<xsl:stylesheet version="1.0" 
     xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
     xmlns:at="http://plone.org/ns/archetypes/"
     xmlns:cmf="http://cmf.zope.org/namespaces/default/"
     xmlns:dc="http://purl.org/dc/elements/1.1/">

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
                    <!-- do some special with 'cmf:workflow_history' element -->
                    <xsl:when test="name()='cmf:workflow_history'">
                        <xsl:copy select=".">
                            <xsl:apply-templates select="cmf:workflow" />
                        </xsl:copy>
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
        <xsl:when test="@name='alwaysOnTop'" />
        <xsl:when test="@name='sendTrackBackURLs'" />
        <!-- change field's name attribute from 'body' to 'text' -->
        <xsl:when test="@name='body'">
            <xsl:copy select=".">
                <xsl:attribute name="name">text</xsl:attribute>
                <xsl:value-of select="." />
            </xsl:copy>
        </xsl:when>
        <!-- change field's name attribute form 'categories' to 'subject' -->
        <xsl:when test="@name='categories'">
            <dc:subject>
                <xsl:value-of select="."/>
            </dc:subject>
        </xsl:when>
        <!-- copy all other elements -->
        <xsl:otherwise>
            <xsl:copy-of select="."/>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

<xsl:template match="cmf:type">
    <xsl:copy select=".">
        <xsl:text>Document</xsl:text>
    </xsl:copy>
</xsl:template>

<xsl:template match="cmf:workflow">
    <xsl:copy select=".">
        <!-- rename 'id' attribute -->
        <xsl:attribute name="id">plone_workflow</xsl:attribute>
        <xsl:copy-of select="cmf:history"/>
    </xsl:copy>
</xsl:template>

</xsl:stylesheet>
