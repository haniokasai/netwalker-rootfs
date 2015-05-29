<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

<!-- This is a customised stylesheet for the Ubuntu Installation Guide to give it a
     different footer to the other Ubuntu documents because it has a different licence -->

<!-- Imports -->
<xsl:import href="ubuntu-html-chunk-cust.xsl"/>	

<!-- This adds the footer -->

<xsl:template name="user.footer.navigation">
<hr />
<div id="footer">

  <div id="ubuntulinks">

	<p>The material in this document is available under the terms of the GNU General Public Licence, see <a href="appendix-gpl.html">Appendix F</a> for details<br />
	To report a problem, file a bug on the <a href="https://bugs.launchpad.net/ubuntu/+source/installation-guide/+filebug">Ubuntu installation-guide package</a></p>

  </div>

</div>

<div id="bottomcap">
	<img src="https://help.ubuntu.com/htdocs/ubuntunew/img/cap-bottom.png" alt=""/>
</div>

</xsl:template>

</xsl:stylesheet>
