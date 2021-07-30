import unittest
from mynodes.hybridanalysis.invokeFalconSandboxWebApi import postFalconSandbox, getFalconSandbox


class TestFalconSandboxMethods(unittest.TestCase):
    def testGenerateFalcoscnSandboxGet(self):
        apiKey = 'c0oko0wcwg8g00cocccckosgsockcosss4g048s0880k0ck4kwsoocs8o4k40goo'
        json_response = getFalconSandbox('https://www.hybrid-analysis.com/api/v2/quick-scan/state',
                                apiKey)
        self.assertIsNotNone(json_response)

    def testGenerateFalcoscnSandboxPost(self):
        apiKey = 'c0oko0wcwg8g00cocccckosgsockcosss4g048s0880k0ck4kwsoocs8o4k40goo'
        data = {
            'url': 'dtonomy.com',
            'scan_type': 'all'
        }
        json_response = postFalconSandbox('https://www.hybrid-analysis.com/api/v2/quick-scan/url-for-analysis',
                                apiKey,
                                data)
        self.assertIsNotNone(json_response['scanners'])

if __name__ == '__main__':
    unittest.main()