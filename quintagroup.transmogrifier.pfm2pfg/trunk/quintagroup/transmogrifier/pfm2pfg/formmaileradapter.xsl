<xsl:stylesheet version="1.0" 
     xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
     xmlns:at="http://plone.org/ns/archetypes/"
     xmlns:cmf="http://cmf.zope.org/namespaces/default/"
     xmlns:dc="http://purl.org/dc/elements/1.1/"
     xmlns:xmp="adobe:ns:meta">

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
                    <!-- remove unnecessary elements -->
                    <xsl:when test="name()='form'" />
                    <xsl:when test="name()='uid'" />
                    <xsl:when test="name()='dc:title'" />
                    <xsl:when test="name()='dc:description'" />
                    <xsl:when test="name()='dc:contributor'" />
                    <xsl:when test="name()='dc:creator'" />
                    <xsl:when test="name()='dc:rights'" />
                    <xsl:when test="name()='dc:language'" />
                    <!--xsl:when test="name()='xmp:CreateDate'" /-->
                    <!-- xsl:when test="name()='xmp:ModifyDate'" /-->
                    <xsl:when test="name()='cmf:type'" />
                    <xsl:when test="name()='cmf:workflow_history'" />
                    <xsl:when test="name()='cmf:security'" />
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
        <!-- next at fields are omitted -->
        <xsl:when test="@name='id'" />
        <xsl:when test="@name='relatedItems'" />
        <xsl:when test="@name='location'" />
        <xsl:when test="@name='effectiveDate'" />
        <xsl:when test="@name='expirationDate'" />
        <xsl:when test="@name='allowDiscussion'" />
        <xsl:when test="@name='excludeFromNav'" />
        <!-- skip zpt of message body, because it can't be used in PFG -->
        <xsl:when test="@name='body_pt'" />

        <!-- change field's name attribute from 'recipient_email' to 'recipientOverride' (TALESString) -->
        <xsl:when test="@name='recipient_email'">
            <xsl:copy select=".">
                <xsl:attribute name="name">recipientOverride</xsl:attribute>
                <xsl:value-of select="." />
            </xsl:copy>
        </xsl:when>
        <!-- change field's name attribute from 'subject' to 'subjectOverride' (TALESString) -->
        <xsl:when test="@name='subject'">
            <xsl:copy select=".">
                <xsl:attribute name="name">subjectOverride</xsl:attribute>
                <xsl:value-of select="." />
            </xsl:copy>
        </xsl:when>

        <xsl:when test="@name='body_type'">
            <xsl:copy select=".">
                <xsl:attribute name="name">body_type</xsl:attribute>
                <xsl:choose>
                    <xsl:when test="contains(string(), 'text/plain')">
                        <xsl:text>plain</xsl:text>
                    </xsl:when>
                    <xsl:when test="contains(string(), 'text/html')">
                        <xsl:text>html</xsl:text>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:text>plain</xsl:text>
                    </xsl:otherwise>
                </xsl:choose>
           </xsl:copy>
        </xsl:when>

        <!-- copy all other elements -->
        <xsl:otherwise>
            <xsl:copy-of select="."/>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

</xsl:stylesheet>
