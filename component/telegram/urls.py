from django.urls import include, path
from rest_framework.routers import DefaultRouter

from component.telegram.views import *

router = DefaultRouter()


router.register(r"send-message", SendMessageViewSet)
router.register(r"forward-message", ForwardMessageViewSet)
router.register(r"forward-messages", ForwardMessagesViewSet)
router.register(r"copy-message", CopyMessageViewSet)
router.register(r"copy-messages", CopyMessagesViewSet)
router.register(r"send-photo", SendPhotoViewSet)
router.register(r"send-document", SendDocumentViewSet)
router.register(r"send-video", SendVideoViewSet)
router.register(r"send-animation", SendAnimationViewSet)
router.register(r"send-voice", SendVoiceViewSet)
router.register(r"send-video-note", SendVideoNoteViewSet)
router.register(r"send-paid-media", SendPaidMediaViewSet)
router.register(r"send-media-group", SendMediaGroupViewSet)
router.register(r"send-location", SendLocationViewSet)
router.register(r"send-venue", SendVenueViewSet)
router.register(r"send-contact", SendContactViewSet)
router.register(r"send-poll", SendPollViewSet)
router.register(r"send-dice", SendDiceViewSet)
router.register(r"set-message-reaction", SetMessageReactionViewSet)
router.register(r"get-user-profile-photos", GetUserProfilePhotosViewSet)
router.register(r"set-user-emoji-status", SetUserEmojiStatusViewSet)
router.register(r"get-file", GetFileViewSet)
router.register(r"ban-chat-member", BanChatMemberViewSet)
router.register(r"unban-chat-member", UnbanChatMemberViewSet)
router.register(r"restrict-chat-member", RestrictChatMemberViewSet)
router.register(r"promote-chat-member", PromoteChatMemberViewSet)
router.register(
    r"set-chat-administrator-custom-title",
    SetChatAdministratorCustomTitleViewSet,
)
router.register(r"ban-chat-sender-chat", BanChatSenderChatViewSet)
router.register(r"unban-chat-sender-chat", UnbanChatSenderChatViewSet)
router.register(r"set-chat-permissions", SetChatPermissionsViewSet)
router.register(r"export-chat-invite-link", ExportChatInviteLinkViewSet)
router.register(r"create-chat-invite-link", CreateChatInviteLinkViewSet)
router.register(r"edit-chat-invite-link", EditChatInviteLinkViewSet)
router.register(
    r"create-chat-subscription-invite-link",
    CreateChatSubscriptionInviteLinkViewSet,
)
router.register(
    r"edit-chat-subscription-invite-link",
    EditChatSubscriptionInviteLinkViewSet,
)
router.register(r"revoke-chat-invite-link", RevokeChatInviteLinkViewSet)
router.register(r"approve-chat-join-request", ApproveChatJoinRequestViewSet)
router.register(r"decline-chat-join-request", DeclineChatJoinRequestViewSet)
router.register(r"set-chat-photo", SetChatPhotoViewSet)
router.register(r"delete-chat-photo", DeleteChatPhotoViewSet)
router.register(r"set-chat-title", SetChatTitleViewSet)
router.register(r"set-chat-description", SetChatDescriptionViewSet)
router.register(r"pin-chat-message", PinChatMessageViewSet)
router.register(r"unpin-chat-message", UnpinChatMessageViewSet)
router.register(r"unpin-all-chat-messages", UnpinAllChatMessagesViewSet)
router.register(r"leave-chat", LeaveChatViewSet)
router.register(r"get-chat", GetChatViewSet)
router.register(r"get-chat-administrators", GetChatAdministratorsViewSet)
router.register(r"get-chat-member-count", GetChatMemberCountViewSet)
router.register(r"get-chat-member", GetChatMemberViewSet)
router.register(r"set-chat-sticker-set", SetChatStickerSetViewSet)
router.register(r"delete-chat-sticker-set", DeleteChatStickerSetViewSet)
router.register(r"create-forum-topic", CreateForumTopicViewSet)
router.register(r"edit-forum-topic", EditForumTopicViewSet)
router.register(r"close-forum-topic", CloseForumTopicViewSet)
router.register(r"reopen-forum-topic", ReopenForumTopicViewSet)
router.register(r"delete-forum-topic", DeleteForumTopicViewSet)
router.register(r"unpin-all-forum-topic-messages", UnpinAllForumTopicMessagesViewSet)
router.register(r"edit-general-forum-topic", EditGeneralForumTopicViewSet)
router.register(r"close-general-forum-topic", CloseGeneralForumTopicViewSet)
router.register(r"reopen-general-forum-topic", ReopenGeneralForumTopicViewSet)
router.register(r"hide-general-forum-topic", HideGeneralForumTopicViewSet)
router.register(r"unhide-general-forum-topic", UnhideGeneralForumTopicViewSet)
router.register(
    r"unpin-all-general-forum-topic-messages",
    UnpinAllGeneralForumTopicMessagesViewSet,
)
router.register(r"get-user-chat-boosts", GetUserChatBoostsViewSet)
router.register(r"get-business-connection", GetBusinessConnectionViewSet)
router.register(r"set-my-commands", SetMyCommandsViewSet)
router.register(r"delete-my-commands", DeleteMyCommandsViewSet)
router.register(r"get-my-commands", GetMyCommandsViewSet)
router.register(r"set-my-name", SetMyNameViewSet)
router.register(r"get-my-name", GetMyNameViewSet)
router.register(r"set-my-description", SetMyDescriptionViewSet)
router.register(r"get-my-description", GetMyDescriptionViewSet)
router.register(r"set-my-short-description", SetMyShortDescriptionViewSet)
router.register(r"get-my-short-description", GetMyShortDescriptionViewSet)
router.register(r"set-chat-menu-button", SetChatMenuButtonViewSet)
router.register(r"get-chat-menu-button", GetChatMenuButtonViewSet)
router.register(
    r"set-my-default-administrator-rights",
    SetMyDefaultAdministratorRightsViewSet,
)
router.register(
    r"get-my-default-administrator-rights",
    GetMyDefaultAdministratorRightsViewSet,
)
router.register(r"edit-message-text", EditMessageTextViewSet)
router.register(r"edit-message-caption", EditMessageCaptionViewSet)
router.register(r"edit-message-media", EditMessageMediaViewSet)
router.register(r"edit-message-live-location", EditMessageLiveLocationViewSet)
router.register(r"stop-message-live-location", StopMessageLiveLocationViewSet)
router.register(r"edit-message-reply-markup", EditMessageReplyMarkupViewSet)
router.register(r"stop-poll", StopPollViewSet)
router.register(r"delete-message", DeleteMessageViewSet)
router.register(r"delete-messages", DeleteMessagesViewSet)
router.register(r"send-gift", SendGiftViewSet)
router.register(r"gift-premium-subscription", GiftPremiumSubscriptionViewSet)
router.register(r"verify-user", VerifyUserViewSet)
router.register(r"verify-chat", VerifyChatViewSet)
router.register(r"remove-user-verification", RemoveUserVerificationViewSet)
router.register(r"remove-chat-verification", RemoveChatVerificationViewSet)
router.register(r"read-business-message", ReadBusinessMessageViewSet)
router.register(r"delete-business-messages", DeleteBusinessMessagesViewSet)
router.register(r"set-business-account-name", SetBusinessAccountNameViewSet)
router.register(r"set-business-account-username", SetBusinessAccountUsernameViewSet)
router.register(r"set-business-account-bio", SetBusinessAccountBioViewSet)
router.register(
    r"set-business-account-profile-photo",
    SetBusinessAccountProfilePhotoViewSet,
)
router.register(
    r"remove-business-account-profile-photo",
    RemoveBusinessAccountProfilePhotoViewSet,
)
router.register(
    r"set-business-account-gift-settings",
    SetBusinessAccountGiftSettingsViewSet,
)
router.register(
    r"get-business-account-star-balance",
    GetBusinessAccountStarBalanceViewSet,
)
router.register(r"transfer-business-account-stars", TransferBusinessAccountStarsViewSet)
router.register(r"get-business-account-gifts", GetBusinessAccountGiftsViewSet)
router.register(r"convert-gift-to-stars", ConvertGiftToStarsViewSet)
router.register(r"upgrade-gift", UpgradeGiftViewSet)
router.register(r"transfer-gift", TransferGiftViewSet)
router.register(r"post-story", PostStoryViewSet)
router.register(r"edit-story", EditStoryViewSet)
router.register(r"delete-story", DeleteStoryViewSet)
router.register(r"send-sticker", SendStickerViewSet)
router.register(r"get-sticker-set", GetStickerSetViewSet)
router.register(r"get-custom-emoji-stickers", GetCustomEmojiStickersViewSet)
router.register(r"upload-sticker-file", UploadStickerFileViewSet)
router.register(r"create-new-sticker-set", CreateNewStickerSetViewSet)
router.register(r"add-sticker-to-set", AddStickerToSetViewSet)
router.register(r"set-sticker-position-in-set", SetStickerPositionInSetViewSet)
router.register(r"delete-sticker-from-set", DeleteStickerFromSetViewSet)
router.register(r"replace-sticker-in-set", ReplaceStickerInSetViewSet)
router.register(r"set-sticker-emoji-list", SetStickerEmojiListViewSet)
router.register(r"set-sticker-keywords", SetStickerKeywordsViewSet)
router.register(r"set-sticker-mask-position", SetStickerMaskPositionViewSet)
router.register(r"set-sticker-set-title", SetStickerSetTitleViewSet)
router.register(r"set-sticker-set-thumbnail", SetStickerSetThumbnailViewSet)
router.register(
    r"set-custom-emoji-sticker-set-thumbnail",
    SetCustomEmojiStickerSetThumbnailViewSet,
)
router.register(r"delete-sticker-set", DeleteStickerSetViewSet)
router.register(r"answer-inline-query", AnswerInlineQueryViewSet)
router.register(r"answer-web-app-query", AnswerWebAppQueryViewSet)
router.register(r"save-prepared-inline-message", SavePreparedInlineMessageViewSet)
router.register(r"send-invoice", SendInvoiceViewSet)
router.register(r"create-invoice-link", CreateInvoiceLinkViewSet)
router.register(r"answer-shipping-query", AnswerShippingQueryViewSet)
router.register(r"answer-pre-checkout-query", AnswerPreCheckoutQueryViewSet)
router.register(r"get-star-transactions", GetStarTransactionsViewSet)
router.register(r"refund-star-payment", RefundStarPaymentViewSet)
router.register(r"edit-user-star-subscription", EditUserStarSubscriptionViewSet)
router.register(r"send-game", SendGameViewSet)
router.register(r"set-game-score", SetGameScoreViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
