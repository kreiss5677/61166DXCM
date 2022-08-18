# Kenton Reiss
# 2022/08/18

# Import necessary libraries
from datetime import datetime
import requests

# Begin function definition for the test suite
def TestSuite(baseURL):
    # Constants
    SUBDIR = "/info"
    EXPECT1 = 200
    EXPECT2 = "application/json"
    PRODUCT3 = "Dexcom API"
    EXPECT3a = "00386270000668"
    EXPECT3b = "3.1.0.0"
    EXPECT3c = "350-0019"
    EXPECT3d = "api-gateway"
    EXPECT3e = "insulin-service"
    EXPECT4 = "application/xml"

    # Concatenate info subdirectory to request correct URL
    fullURL = baseURL + SUBDIR

    # Set up string for current time and date
    currTime = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    # Attempt to request response from provided URL
    try:
        response = requests.get(fullURL)
        validURL = True
        title = currTime + " || Test Suite Run on " + baseURL
    except:
        validURL = False
        title = currTime + " || TEST SUITE RUN ON " + baseURL + " ABORTED"

    # Log whether test run starts or not
    print(title)

    # Check if URL is valid before performing tests
    if validURL:
        # Attempt to get value from header (in this case, content type)
        try:
            con_type = response.headers["Content-Type"]
        except:
            con_type = "NULL"
        
        # TEST 1
        # Attempt to get status code from request
        try:
            code = response.status_code
        except:
            code = -1
        # Check status code against valid value
        if code == EXPECT1:
            pORf = "PASS"
        else:
            pORf = "FAIL"
        # Log results of first test
        result1 = "-Test #1, Status Code- Expected: " + str(EXPECT1) + " Actual: " + str(code) + " || " + pORf
        print(result1)
        
        # TEST 2
        # Check content type against desired type
        if con_type == EXPECT2:
            pORf = "PASS"
        else:
            pORf = "FAIL"
        # Log results of second test
        result2 = "-Test #2, Content Type- Expected: " + EXPECT2 + " Actual: " + con_type + " || " + pORf
        print(result2)

        # TEST 3
        # Attempt to acquire content from API
        try:
            content = response.json()
            con_avail = True
        except:
            con_avail = False
            result3 = "-Test #3- CONTENT NOT AVAILABLE || FAIL"
            print(result3)

        if con_avail:
            # Look for specified product name
            thisProd = None
            try:
                for prod in content:
                    if prod["Product Name"] == PRODUCT3:
                        thisProd = prod
            except:
                thisProd = None

            # If product name is not found, test fails
            if thisProd == None:
                result3 = "-Test #3- " + PRODUCT3 + " NOT FOUND || FAIL"
                print(result3)
            # Otherwise, sub-tests proceed
            else:
                # Log that the product was found
                result3 = "-Test #3- " + PRODUCT3 + " FOUND"
                print(result3)
                
                # TEST 3a
                # Attempt to acquire the product's UDI
                try:
                    UDI = thisProd["UDI / Device Identifier"]
                except:
                    UDI = "NULL"
                # Check UDI against desired value
                if UDI == EXPECT3a:
                    pORf = "PASS"
                else:
                    pORf = "FAIL"
                # Log 3a test results
                result3a = "-Test #3a, UDI- Expected: " + EXPECT3a + " Actual: " + UDI + " || " + pORf
                print(result3a)

                # TEST 3b
                # Attempt to acquire the product's identifier's version
                try:
                    ver = thisProd["UDI / Production Identifier"]["Version"]
                except:
                    ver = "NULL"
                # Check version against desired value
                if ver == EXPECT3b:
                    pORf = "PASS"
                else:
                    pORf = "FAIL"
                # Log 3b test results
                result3b = "-Test #3b, Version- Expected: " + EXPECT3b + " Actual: " + ver + " || " + pORf
                print(result3b)
                    
                # TEST 3c
                # Attempt to acquire the product's identifier's part number
                try:
                    PN = thisProd["UDI / Production Identifier"]["Part Number (PN)"]
                except:
                    PN = "NULL"
                # Check PN against desired value
                if PN == EXPECT3c:
                    pORf = "PASS"
                else:
                    pORf = "FAIL"
                # Log 3c test results
                result3c = "-Test #3c, PN- Expected: " + EXPECT3c + " Actual: " + PN + " || " + pORf
                print(result3c)

                # Attempt to access the product's identifier's sub-components
                try:
                    sub = thisProd["UDI / Production Identifier"]["Sub-Components"]
                    sub_exist = True
                except:
                    sub_exist = False
                # If sub-components exist, look for the desired names
                if sub_exist:
                    # TESTS 3d & 3e
                    try:
                        b_3d = b_3e = False
                        for obj in sub:
                            # Look in every sub-component for matching names
                            if EXPECT3d == obj["Name"]:
                                b_3d = True
                            if EXPECT3e == obj["Name"]:
                                b_3e = True
                    # If sub-components cause exception, fail the cases
                    except:
                        result3f = "-Tests #3d & 3e, Names- No/Incorrect Sub-Components || FAIL"
                        print(result3f)

                    # Log 3d test results
                    if b_3d:
                        result3d = "-Test #3d, Name- " + EXPECT3d + " is present || PASS"
                    else:
                        result3d = "-Test #3d, Name- " + EXPECT3d + " is not present || FAIL"
                    print(result3d)
                    # Log 3e test results    
                    if b_3e:
                        result3e = "-Test #3e, Name- " + EXPECT3e + " is present || PASS"
                    else:
                        result3e = "-Test #3e, Name- " + EXPECT3e + " is not present || FAIL"
                    print(result3e)

        # TEST 4
        # Check content type against desired type
        if con_type == EXPECT4:
            pORf = "PASS"
        else:
            pORf = "FAIL"
        # Log results of fourth test
        result4 = "-Test #4, Content Type- Expected: " + EXPECT4 + " Actual: " + con_type + " || " + pORf
        print(result4)

    # Print new line to separate results from other runs
    print()

# Run the tests on different URLs
TestSuite("https://api.dexcom.com")
TestSuite("https://sandbox-api.dexcom.com")

# Uncomment this line for demo of workflow with invalid URL (wait for timeout)
# TestSuite("https://thisisnotarealURL.gov")
