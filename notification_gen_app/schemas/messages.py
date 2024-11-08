from pydantic import BaseModel, EmailStr, AnyUrl


class InstantMessageRequest(BaseModel):
    email: EmailStr
    message_data: dict


class WelcomeMessageRequest(BaseModel):
    message_data: dict


class WelcomeLinkMessageRequest(BaseModel):
    message_data: dict
    confirmation_link: AnyUrl
