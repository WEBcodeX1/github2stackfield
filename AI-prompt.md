Build an x0 application using the x0 framework from https://github.com/WEBcodeX1/x0,
The backend in Python should use the https://github.com/clauspruefer/python-micro-esb project
The CSS styling is done with the x0 contained Bootstrap default theme and should look modern.
The browser-frontend consists of 3 x0 screens / 3 menu entries:
1. Screen1 "User Credentials": contains 2 groups of formfields (x0 object of type `sysObjectFormfieldList`): group a) GitHub API User/Token credentials group b) Stackfield API User/Token Credentials
1.1. On each formfield group there must be a button "verify user credentials" to test if the API authentication is working
2. Screen2 "Issue / Task Mapping": contains the mapping between GitHub Issues and Stackfield Tasks
2.1. On top there should be 1 formfield / search input and a search execution button (x0 object of type `sysObjectFormfieldList`)
2.2. Under the search must be a list (x0 object of type `sysObjectList` containing the search results
2.3. The search result list from 2.2. contains a x0 object of type `sysObjContextMenu` with one entry "Connect Stackfield Task"
2.4. On button click from 2.1 the relevant python-micro-esb backend service must be called and the given result list from 2.2 must be filled with the result data from the backend service
3. Screen3 "Connect Stackfield Task"
3.1. Contains detailed GitHub Task properties from GitHub API webservice result (encapsulated from python-micro-esb backend), e.g. 3 or four formfields describing the task properties from API result
3.2. On right click of screen 2 object result display list single row, the GitHub task properties fields of Screen3 will be updated from the row data
3.3. Also there should be relevant Stackfield properties where to map the Stackfield Task (Stackfield room or similar, please find the best possible fields from the API to map)
3.4. At the bottom there must be 1 button (x0 object type `sysObjButton`), on click a NEW STACKFIELD TASK will be generated from the relevant GitHub Issue/Task data from Screen3 formfield data.
