from rest_framework import serializers

from component.models import *


class SendMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendMessage
        depth = 1
        fields = "__all__"


class ForwardMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForwardMessage
        depth = 1
        fields = "__all__"


class ForwardMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForwardMessages
        depth = 1
        fields = "__all__"


class CopyMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CopyMessage
        depth = 1
        fields = "__all__"


class CopyMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CopyMessages
        depth = 1
        fields = "__all__"


class SendPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendPhoto
        depth = 1
        fields = "__all__"


class SendDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendDocument
        depth = 1
        fields = "__all__"


class SendVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendVideo
        depth = 1
        fields = "__all__"


class SendAnimationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendAnimation
        depth = 1
        fields = "__all__"


class SendVoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendVoice
        depth = 1
        fields = "__all__"


class SendVideoNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendVideoNote
        depth = 1
        fields = "__all__"


class SendPaidMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendPaidMedia
        depth = 1
        fields = "__all__"


class SendMediaGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendMediaGroup
        depth = 1
        fields = "__all__"


class SendLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendLocation
        depth = 1
        fields = "__all__"


class SendVenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendVenue
        depth = 1
        fields = "__all__"


class SendContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendContact
        depth = 1
        fields = "__all__"


class SendPollSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendPoll
        depth = 1
        fields = "__all__"


class SendDiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendDice
        depth = 1
        fields = "__all__"


class SetMessageReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetMessageReaction
        depth = 1
        fields = "__all__"


class GetUserProfilePhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetUserProfilePhotos
        depth = 1
        fields = "__all__"


class SetUserEmojiStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetUserEmojiStatus
        depth = 1
        fields = "__all__"


class GetFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetFile
        depth = 1
        fields = "__all__"


class BanChatMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = BanChatMember
        depth = 1
        fields = "__all__"


class UnbanChatMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnbanChatMember
        depth = 1
        fields = "__all__"


class RestrictChatMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestrictChatMember
        depth = 1
        fields = "__all__"


class PromoteChatMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoteChatMember
        depth = 1
        fields = "__all__"


class SetChatAdministratorCustomTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetChatAdministratorCustomTitle
        depth = 1
        fields = "__all__"


class BanChatSenderChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = BanChatSenderChat
        depth = 1
        fields = "__all__"


class UnbanChatSenderChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnbanChatSenderChat
        depth = 1
        fields = "__all__"


class SetChatPermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetChatPermissions
        depth = 1
        fields = "__all__"


class ExportChatInviteLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExportChatInviteLink
        depth = 1
        fields = "__all__"


class CreateChatInviteLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateChatInviteLink
        depth = 1
        fields = "__all__"


class EditChatInviteLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = EditChatInviteLink
        depth = 1
        fields = "__all__"


class CreateChatSubscriptionInviteLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateChatSubscriptionInviteLink
        depth = 1
        fields = "__all__"


class EditChatSubscriptionInviteLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = EditChatSubscriptionInviteLink
        depth = 1
        fields = "__all__"


class RevokeChatInviteLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = RevokeChatInviteLink
        depth = 1
        fields = "__all__"


class ApproveChatJoinRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApproveChatJoinRequest
        depth = 1
        fields = "__all__"


class DeclineChatJoinRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeclineChatJoinRequest
        depth = 1
        fields = "__all__"


class SetChatPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetChatPhoto
        depth = 1
        fields = "__all__"


class DeleteChatPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeleteChatPhoto
        depth = 1
        fields = "__all__"


class SetChatTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetChatTitle
        depth = 1
        fields = "__all__"


class SetChatDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetChatDescription
        depth = 1
        fields = "__all__"


class PinChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PinChatMessage
        depth = 1
        fields = "__all__"


class UnpinChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnpinChatMessage
        depth = 1
        fields = "__all__"


class UnpinAllChatMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnpinAllChatMessages
        depth = 1
        fields = "__all__"


class LeaveChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveChat
        depth = 1
        fields = "__all__"


class GetChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetChat
        depth = 1
        fields = "__all__"


class GetChatAdministratorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetChatAdministrators
        depth = 1
        fields = "__all__"


class GetChatMemberCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetChatMemberCount
        depth = 1
        fields = "__all__"


class GetChatMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetChatMember
        depth = 1
        fields = "__all__"


class SetChatStickerSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetChatStickerSet
        depth = 1
        fields = "__all__"


class DeleteChatStickerSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeleteChatStickerSet
        depth = 1
        fields = "__all__"


class CreateForumTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateForumTopic
        depth = 1
        fields = "__all__"


class EditForumTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = EditForumTopic
        depth = 1
        fields = "__all__"


class CloseForumTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloseForumTopic
        depth = 1
        fields = "__all__"


class ReopenForumTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReopenForumTopic
        depth = 1
        fields = "__all__"


class DeleteForumTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeleteForumTopic
        depth = 1
        fields = "__all__"


class UnpinAllForumTopicMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnpinAllForumTopicMessages
        depth = 1
        fields = "__all__"


class EditGeneralForumTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = EditGeneralForumTopic
        depth = 1
        fields = "__all__"


class CloseGeneralForumTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloseGeneralForumTopic
        depth = 1
        fields = "__all__"


class ReopenGeneralForumTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReopenGeneralForumTopic
        depth = 1
        fields = "__all__"


class HideGeneralForumTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = HideGeneralForumTopic
        depth = 1
        fields = "__all__"


class UnhideGeneralForumTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnhideGeneralForumTopic
        depth = 1
        fields = "__all__"


class UnpinAllGeneralForumTopicMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnpinAllGeneralForumTopicMessages
        depth = 1
        fields = "__all__"


class GetUserChatBoostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetUserChatBoosts
        depth = 1
        fields = "__all__"


class GetBusinessConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetBusinessConnection
        depth = 1
        fields = "__all__"


class SetMyCommandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetMyCommands
        depth = 1
        fields = "__all__"


class DeleteMyCommandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeleteMyCommands
        depth = 1
        fields = "__all__"


class GetMyCommandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetMyCommands
        depth = 1
        fields = "__all__"


class SetMyNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetMyName
        depth = 1
        fields = "__all__"


class GetMyNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetMyName
        depth = 1
        fields = "__all__"


class SetMyDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetMyDescription
        depth = 1
        fields = "__all__"


class GetMyDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetMyDescription
        depth = 1
        fields = "__all__"


class SetMyShortDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetMyShortDescription
        depth = 1
        fields = "__all__"


class GetMyShortDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetMyShortDescription
        depth = 1
        fields = "__all__"


class SetChatMenuButtonSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetChatMenuButton
        depth = 1
        fields = "__all__"


class GetChatMenuButtonSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetChatMenuButton
        depth = 1
        fields = "__all__"


class SetMyDefaultAdministratorRightsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetMyDefaultAdministratorRights
        depth = 1
        fields = "__all__"


class GetMyDefaultAdministratorRightsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetMyDefaultAdministratorRights
        depth = 1
        fields = "__all__"


class EditMessageTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = EditMessageText
        depth = 1
        fields = "__all__"


class EditMessageCaptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EditMessageCaption
        depth = 1
        fields = "__all__"


class EditMessageMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EditMessageMedia
        depth = 1
        fields = "__all__"


class EditMessageLiveLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EditMessageLiveLocation
        depth = 1
        fields = "__all__"


class StopMessageLiveLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StopMessageLiveLocation
        depth = 1
        fields = "__all__"


class EditMessageReplyMarkupSerializer(serializers.ModelSerializer):
    class Meta:
        model = EditMessageReplyMarkup
        depth = 1
        fields = "__all__"


class StopPollSerializer(serializers.ModelSerializer):
    class Meta:
        model = StopPoll
        depth = 1
        fields = "__all__"


class DeleteMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeleteMessage
        depth = 1
        fields = "__all__"


class DeleteMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeleteMessages
        depth = 1
        fields = "__all__"


class SendStickerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendSticker
        depth = 1
        fields = "__all__"


class GetStickerSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetStickerSet
        depth = 1
        fields = "__all__"


class GetCustomEmojiStickersSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetCustomEmojiStickers
        depth = 1
        fields = "__all__"


class UploadStickerFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadStickerFile
        depth = 1
        fields = "__all__"


class CreateNewStickerSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateNewStickerSet
        depth = 1
        fields = "__all__"


class AddStickerToSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddStickerToSet
        depth = 1
        fields = "__all__"


class SetStickerPositionInSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetStickerPositionInSet
        depth = 1
        fields = "__all__"


class DeleteStickerFromSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeleteStickerFromSet
        depth = 1
        fields = "__all__"


class ReplaceStickerInSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplaceStickerInSet
        depth = 1
        fields = "__all__"


class SetStickerEmojiListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetStickerEmojiList
        depth = 1
        fields = "__all__"


class SetStickerKeywordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetStickerKeywords
        depth = 1
        fields = "__all__"


class SetStickerMaskPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetStickerMaskPosition
        depth = 1
        fields = "__all__"


class SetStickerSetTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetStickerSetTitle
        depth = 1
        fields = "__all__"


class SetStickerSetThumbnailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetStickerSetThumbnail
        depth = 1
        fields = "__all__"


class SetCustomEmojiStickerSetThumbnailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetCustomEmojiStickerSetThumbnail
        depth = 1
        fields = "__all__"


class DeleteStickerSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeleteStickerSet
        depth = 1
        fields = "__all__"


class SendGiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendGift
        depth = 1
        fields = "__all__"


class VerifyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifyUser
        depth = 1
        fields = "__all__"


class VerifyChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifyChat
        depth = 1
        fields = "__all__"


class RemoveUserVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RemoveUserVerification
        depth = 1
        fields = "__all__"


class RemoveChatVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RemoveChatVerification
        depth = 1
        fields = "__all__"


class AnswerInlineQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerInlineQuery
        depth = 1
        fields = "__all__"


class AnswerWebAppQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerWebAppQuery
        depth = 1
        fields = "__all__"


class SavePreparedInlineMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavePreparedInlineMessage
        depth = 1
        fields = "__all__"


class SendInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendInvoice
        depth = 1
        fields = "__all__"


class CreateInvoiceLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateInvoiceLink
        depth = 1
        fields = "__all__"


class AnswerShippingQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerShippingQuery
        depth = 1
        fields = "__all__"


class AnswerPreCheckoutQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerPreCheckoutQuery
        depth = 1
        fields = "__all__"


class GetStarTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetStarTransactions
        depth = 1
        fields = "__all__"


class RefundStarPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefundStarPayment
        depth = 1
        fields = "__all__"


class EditUserStarSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EditUserStarSubscription
        depth = 1
        fields = "__all__"


class SendGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendGame
        depth = 1
        fields = "__all__"


class SetGameScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetGameScore
        depth = 1
        fields = "__all__"


class IfComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = IfComponent
        depth = 1
        fields = "__all__"


class SwitchComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SwithComponent
        depth = 1
        fields = "__all__"


class CodeComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeComponent
        depth = 1
        fields = "__all__"
