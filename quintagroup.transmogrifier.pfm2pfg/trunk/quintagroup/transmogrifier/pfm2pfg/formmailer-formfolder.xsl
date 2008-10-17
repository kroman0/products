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
                    <!-- skip 'cmf:workflow_history' element (PFG has another workflow) -->
                    <xsl:when test="name()='cmf:workflow_history'" />
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
        <xsl:when test="@name='before_script'" />
        <xsl:when test="@name='form_buttons'" />

        <!-- change field's name attribute from 'body' to 'text' -->
        <xsl:when test="@name='form_pre'">
            <xsl:copy select=".">
                <xsl:attribute name="name">formPrologue</xsl:attribute>
                <xsl:value-of select="." />
            </xsl:copy>
        </xsl:when>
        <!-- change field's name attribute from 'form_post' to 'text' -->
        <xsl:when test="@name='form_post'">
            <xsl:copy select=".">
                <xsl:attribute name="name">formEpilogue</xsl:attribute>
                <xsl:value-of select="." />
            </xsl:copy>
        </xsl:when>
        <xsl:when test="@name='sent_redirect'">
            <xsl:copy select=".">
                <xsl:attribute name="name">thanksPageOverride</xsl:attribute>
                <xsl:value-of select="." />
            </xsl:copy>
        </xsl:when>
        <xsl:when test="@name='cpyaction'">
            <xsl:copy select=".">
                <xsl:attribute name="name">afterValidationOverride</xsl:attribute>
                <xsl:value-of select="." />
            </xsl:copy>
        </xsl:when>
        <!-- copy all other elements -->
        <xsl:otherwise>
            <xsl:copy-of select="."/>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

<xsl:template match="cmf:type">
    <xsl:copy select=".">
        <xsl:text>FormFolder</xsl:text>
    </xsl:copy>
</xsl:template>

</xsl:stylesheet>
