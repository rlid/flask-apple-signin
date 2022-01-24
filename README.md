# flask-apple-signin
Flask example of "Sign in with Apple" implemented as a tiny extension to Authlib

It is fully working (and closely follows the current specs of Sign in with Apple), but I have left in all the print statements for understanding the protocol and debugging.

The code is uploaded to GitHub in the hope that people might point out:
 - issues that break the basic functionality as the specs of Authlib & Sign in with Apple evolve
 - potential problems that might not affect the functionality in common scenarios but do not conform to the specs of Authlib / Sign in with Apple 

#References
https://developer.apple.com/documentation/sign_in_with_apple/generate_and_validate_tokens
https://github.com/lepture/authlib
https://docs.authlib.org/en/latest/client/oauth2.html