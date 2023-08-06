import unittest
from hdistill.pipeline.html_parser import HtmlParser

class HtmlParserTests(unittest.TestCase):

    def test_parse_html_returns_expected_list(self):
        html_parser = HtmlParser()
        parsed = html_parser.parse_html(test_data, '//td[@class="titleColumn"]/text() | //td[@class="titleColumn"]//a/text() | //td[@class="titleColumn"]//a/@title | //td[@class="titleColumn"]//span[@class="secondaryInfo"]/text()')
        self.assertIn('Frank Darabont (dir.), Tim Robbins, Morgan Freeman', parsed)
        self.assertIn('The Shawshank Redemption', parsed)
        self.assertIn('(1994)', parsed)

test_data = """
<tr>
    <td class="posterColumn">

    <span name="rk" data-value="1"></span>
    <span name="ir" data-value="9.220075738292811"></span>
    <span name="us" data-value="7.791552E11"></span>
    <span name="nv" data-value="2416800"></span>
    <span name="ur" data-value="-1.7799242617071886"></span>
<a href="https://www.imdb.com/title/tt0111161/?pf_rd_m=A2FGELUUNOQJNL&amp;pf_rd_p=e31d89dd-322d-4646-8962-327b42fe94b1&amp;pf_rd_r=0YG0BZZFTS61TBHT80ND&amp;pf_rd_s=center-1&amp;pf_rd_t=15506&amp;pf_rd_i=top&amp;ref_=chttp_tt_1"> <img src="./IMDb Top 250 - IMDb_files/MV5BMDFkYTc0MGEtZmNhMC00ZDIzLWFmNTEtODM1ZmRlYWMwMWFmXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_UY67_CR0,0,45,67_AL_.jpg" width="45" height="67" alt="The Shawshank Redemption">
</a>    </td>
    <td class="titleColumn">
      1.
      <a href="https://www.imdb.com/title/tt0111161/?pf_rd_m=A2FGELUUNOQJNL&amp;pf_rd_p=e31d89dd-322d-4646-8962-327b42fe94b1&amp;pf_rd_r=0YG0BZZFTS61TBHT80ND&amp;pf_rd_s=center-1&amp;pf_rd_t=15506&amp;pf_rd_i=top&amp;ref_=chttp_tt_1" title="Frank Darabont (dir.), Tim Robbins, Morgan Freeman">The Shawshank Redemption</a>
        <span class="secondaryInfo">(1994)</span>
    </td>
    <td class="ratingColumn imdbRating">
            <strong title="9.2 based on 2,416,800 user ratings">9.2</strong>
    </td>
    <td class="ratingColumn">
    <div class="seen-widget seen-widget-tt0111161" data-titleid="tt0111161">
        <div class="boundary">
            <div class="popover">
"""
