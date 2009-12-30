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
        <xsl:when test="@name='existingCats'" />
        <xsl:when test="@name='categories'" />
        <!-- copy all other elements -->
        <xsl:otherwise>
            <xsl:copy-of select="."/>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

<xsl:template match="cmf:type">
    <xsl:copy select=".">
        <xsl:text>Large Plone Folder</xsl:text>
    </xsl:copy>
</xsl:template>

<xsl:template match="cmf:workflow">
    <xsl:copy select=".">
        <!-- rename 'id' attribute -->
        <xsl:attribute name="id">simple_publication_workflow</xsl:attribute>
        <xsl:for-each select="*|text()">
            <xsl:choose>
                <!-- do some special with 'cmf:workflow_history' element -->
                <xsl:when test="name()='cmf:history'">
                    <xsl:copy select=".">
                        <xsl:apply-templates select="cmf:var" />
                    </xsl:copy>
                </xsl:when>
                <!-- copy all other elements -->
                <xsl:otherwise>
                    <xsl:copy-of select="."/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:for-each>
    </xsl:copy>
</xsl:template>

<xsl:template match="cmf:var">
    <xsl:choose>
        <xsl:when test="@value='visible'">
            <xsl:copy select=".">
                <xsl:attribute name="id">review_state</xsl:attribute>
                <xsl:attribute name="type">str</xsl:attribute>
                <xsl:attribute name="value">published</xsl:attribute>
                <xsl:value-of select="." />
            </xsl:copy>
        </xsl:when>
        <!-- copy all other elements -->
        <xsl:otherwise>
            <xsl:copy-of select="."/>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

</xsl:stylesheet>
