## ADDED Requirements
### Requirement: Phone Number Registration
Users SHALL be able to register using their phone number.

#### Scenario: New user registration
- **WHEN** a new user provides a valid phone number
- **THEN** the system SHALL send a verification code to that number

#### Scenario: Invalid phone number
- **WHEN** a user provides an invalid phone number format
- **THEN** the system SHALL return an error message

### Requirement: Verification Code Authentication
Users SHALL be able to authenticate using a verification code sent to their registered phone number.

#### Scenario: Successful verification
- **WHEN** a user provides a valid phone number and correct verification code
- **THEN** the system SHALL create an authenticated session for the user

#### Scenario: Expired verification code
- **WHEN** a user provides a valid phone number but an expired verification code
- **THEN** the system SHALL return an error and prompt for a new code

#### Scenario: Invalid verification code
- **WHEN** a user provides a valid phone number but incorrect verification code
- **THEN** the system SHALL return an error message

### Requirement: Verification Code Generation
The system SHALL generate a 6-digit numeric verification code when a user requests authentication.

#### Scenario: Code generation
- **WHEN** a user requests authentication with a valid phone number
- **THEN** the system SHALL generate a 6-digit numeric verification code

#### Scenario: Code expiration
- **WHEN** a verification code is generated
- **THEN** the code SHALL expire after 10 minutes

### Requirement: Rate Limiting
The system SHALL limit verification code requests to prevent abuse.

#### Scenario: Rate limit exceeded
- **WHEN** a user requests verification codes more than 5 times in 10 minutes
- **THEN** the system SHALL block further requests and return an error