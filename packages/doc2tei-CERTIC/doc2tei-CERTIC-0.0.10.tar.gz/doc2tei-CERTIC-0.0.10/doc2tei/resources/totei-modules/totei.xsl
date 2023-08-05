<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="2.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
  xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
  xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
  xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
  xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
  xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
  xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0"
  xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0" 
  xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0" 
  xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0" 
  xmlns:math="http://www.w3.org/1998/Math/MathML" 
  xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0" 
  xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0" 
  xmlns:config="urn:oasis:names:tc:opendocument:xmlns:config:1.0" 
  xmlns:ooo="http://openoffice.org/2004/office" 
  xmlns:ooow="http://openoffice.org/2004/writer" 
  xmlns:oooc="http://openoffice.org/2004/calc" 
  xmlns:dom="http://www.w3.org/2001/xml-events" 
  xmlns:xforms="http://www.w3.org/2002/xforms" 
  xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
  xmlns:rpt="http://openoffice.org/2005/report" 
  xmlns:of="urn:oasis:names:tc:opendocument:xmlns:of:1.2" 
  xmlns:xhtml="http://www.w3.org/1999/xhtml" 
  xmlns:grddl="http://www.w3.org/2003/g/data-view#" 
  xmlns:officeooo="http://openoffice.org/2009/office" 
  xmlns:tableooo="http://openoffice.org/2009/table" 
  xmlns:drawooo="http://openoffice.org/2010/draw" 
  xmlns:calcext="urn:org:documentfoundation:names:experimental:calc:xmlns:calcext:1.0" 
  xmlns:loext="urn:org:documentfoundation:names:experimental:office:xmlns:loext:1.0" 
  xmlns:field="urn:openoffice:names:experimental:ooo-ms-interop:xmlns:field:1.0" 
  xmlns:formx="urn:openoffice:names:experimental:ooxml-odf-interop:xmlns:form:1.0" 
  xmlns:css3t="http://www.w3.org/TR/css3-text/"
  xmlns="http://www.tei-c.org/ns/1.0"
  exclude-result-prefixes="office style text table draw fo xlink dc meta number svg chart  dr3d math form script config ooo ooow oooc dom xforms xsd xsi rpt of xhtml grddl officeooo tableooo drawooo calcext loext field formx css3t">
    
<xsl:output method="xml" encoding="UTF-8" indent="yes"/>

<!-- template de sauvegarde : ne devrait pas être employé… -->
<xsl:template match="@*|node()">
  <xsl:copy>
    <xsl:apply-templates select="@*|node()"/>
  </xsl:copy>
</xsl:template>

<xsl:include href="core_typo.xsl"/>
<xsl:include href="core_div-para.xsl"/>
<xsl:include href="core_table.xsl"/>
<xsl:include href="core_note.xsl"/>
<xsl:include href="core_quote.xsl"/>
<xsl:include href="core_linking.xsl"/>
<xsl:include href="back_biblio.xsl"/>
    
<xsl:template match="/">
  <TEI>
<!--       change="metopes_edition"  -->
    <teiHeader>
      <fileDesc>
        <titleStmt>
          <title type="main">template de validation</title>
        </titleStmt>
        <editionStmt>
          <edition>
            <date></date>
          </edition>
        </editionStmt>
        <publicationStmt>
          <ab type="papier">
            <dimensions>
              <dim type="pagination"/>
            </dimensions>
            <date/>
          </ab>          
          <idno type="book"/>
          <ab type="lodel">
            <date/>
          </ab>
        </publicationStmt>
        <sourceDesc>
          <p>Version métopes : 2.0</p>
          <p>Written by OpenOffice</p>
        </sourceDesc>
      </fileDesc>
      <encodingDesc>
        <tagsDecl>
          <rendition scheme="css" xml:id="none">color:black;</rendition>
        </tagsDecl>
      </encodingDesc>
      <profileDesc>
        <langUsage>
          <language ident="fr-fr"/>
        </langUsage>
        <textClass/>
      </profileDesc>
      <revisionDesc>
        <change when="2021-02-26T11:25:00" who="C.E">Révision</change>
      </revisionDesc>
    </teiHeader>
    <text>
<!--         xml:id="text"-->
      <front>
      </front>
      <body>
        <xsl:apply-templates select="//*:div[@type='section1']"/>
      </body>
      <xsl:if test="//*:div[@type='bibliography']">
        <back>
          <xsl:apply-templates select="//*:div[@type='bibliography']"/>
        </back>
      </xsl:if>
    </text>
  </TEI>
</xsl:template>

</xsl:stylesheet>