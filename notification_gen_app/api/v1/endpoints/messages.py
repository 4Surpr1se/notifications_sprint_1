from fastapi import Depends, APIRouter, HTTPException
from config.settings import settings
from notification_gen_app.api.v1.dependencies import get_message_service, get_user_info
from notification_gen_app.schemas.messages import InstantMessageRequest, WelcomeMessageRequest, \
    WelcomeLinkMessageRequest
from notification_gen_app.services.messages import MessageService
from notification_gen_app.utils.short_links import generate_confirmation_link
from uuid import UUID

router = APIRouter()


# Endpoint for creating an instant message
@router.post("/instant_messages/{content_id}/")
async def create_instant_message(
        content_id: UUID,
        message: InstantMessageRequest,
        message_service: MessageService = Depends(get_message_service)
):
    try:
        result = await message_service.send_single_message(content_id, message, 'email', settings.instant_message_queue)
        return result
    except HTTPException as e:
        raise e  # Propagate HTTPException to FastAPI's error handler
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


# Endpoint for sending a welcome message
@router.post("/welcome_message/")
async def create_welcome_message(
        message: WelcomeMessageRequest,
        message_service: MessageService = Depends(get_message_service),
        user_info: dict = Depends(get_user_info)
):
    try:
        email = user_info.get('email')
        user_id = user_info.get('sub')
        confirmation_link = generate_confirmation_link(user_id, settings.redirect_url, settings.expires_in)

        message_data = message.message_data
        message_data['confirmation_link'] = confirmation_link

        result = await message_service.send_welcome_message(email, message_data, 'email',
                                                            settings.instant_message_queue)
        return result
    except HTTPException as e:
        raise e  # Propagate HTTPException to FastAPI's error handler
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")