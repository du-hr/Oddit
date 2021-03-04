Feature: Add New User

As a SSMU employee
I would like become a user of the Oddit Web Application System
So that I can plan budgets for my club

Scenario Outline: Different types of users (Normal Flow)

Given SSMU employee <ex_name> with student id <st_id> is an employee of type <ex_type> in club <club_name> in good standing
When employee <ex_name> requests user access to the Oddit Web Application System
Then a new <user_name> and initial <password> are generated

| ex_name        | st_id  | ex_type    | club_name   |user_name | password |
| Archie Andrews |AA001   |President   |MDU          |Andrews_A |aa001     |
| Betty Cooper   |CB002   |Treasurer   |MDU			 |Cooper_B  |cb002     |
| Jughead Jones  |JJ003   |Treasurer   |ECSESS 		 |Jones_J   |jj003     |
| Veronica Lodge |LV004   |President   |ECSESS       |Lodge_V   |lv004     |
| Reggie Mantle  |MR005   |President   |MRT   		 |Mantle_R  |mr005     |
| Ethel Mudd     |ME006   |Treasurer   |MRT		     |me006     |mr007     |

Scenario Outline: Non SSMU employee attempts to become user (Error Flow)

Given Fred Smith uses id INVALID_ID to request Treasurer user access
When Fred Smith requests user access to the Oddit Web Application System
Then an "Unauthorized request" message is issued

Scenario Outline: Existing user attempts to become a user (Error Flow)

Given Bill Jones is user with student id 11111 of the Oddit Web Application System
When Bill Jones with student id 11111 requests user access to the Oddit Web Application System
Then an "Already registered" message is issued

Scenario Outline: Attempts to become a user with incomplete information (Error Flow)

Given Drake does not enter his name in the Oddit Web Application System
When Drake requests user access to the Oddit Web Application System
Then an "Incomplete information" message is issued

