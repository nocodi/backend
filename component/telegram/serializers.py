from rest_framework import serializers

from component.telegram.models import *


class ModelSerializerCustom(serializers.ModelSerializer):
    def create(self, validated_data: dict) -> Component:
        validated_data["bot_id"] = self.context.get("bot")
        return super().create(validated_data)


class SendMessageSerializer(ModelSerializerCustom):
    class Meta:
        model = SendMessage
        exclude = ["component_type", "bot"]


class ForwardMessageSerializer(ModelSerializerCustom):
    class Meta:
        model = ForwardMessage
        exclude = ["component_type", "bot"]


class ForwardMessagesSerializer(ModelSerializerCustom):
    class Meta:
        model = ForwardMessages
        exclude = ["component_type", "bot"]


class CopyMessageSerializer(ModelSerializerCustom):
    class Meta:
        model = CopyMessage
        exclude = ["component_type", "bot"]


class CopyMessagesSerializer(ModelSerializerCustom):
    class Meta:
        model = CopyMessages
        exclude = ["component_type", "bot"]


class SendPhotoSerializer(ModelSerializerCustom):
    class Meta:
        model = SendPhoto
        exclude = ["component_type", "bot"]


class SendDocumentSerializer(ModelSerializerCustom):
    class Meta:
        model = SendDocument
        exclude = ["component_type", "bot"]


class SendVideoSerializer(ModelSerializerCustom):
    class Meta:
        model = SendVideo
        exclude = ["component_type", "bot"]


class SendAnimationSerializer(ModelSerializerCustom):
    class Meta:
        model = SendAnimation
        exclude = ["component_type", "bot"]


class SendVoiceSerializer(ModelSerializerCustom):
    class Meta:
        model = SendVoice
        exclude = ["component_type", "bot"]


class SendVideoNoteSerializer(ModelSerializerCustom):
    class Meta:
        model = SendVideoNote
        exclude = ["component_type", "bot"]


class SendPaidMediaSerializer(ModelSerializerCustom):
    class Meta:
        model = SendPaidMedia
        exclude = ["component_type", "bot"]


class SendMediaGroupSerializer(ModelSerializerCustom):
    class Meta:
        model = SendMediaGroup
        exclude = ["component_type", "bot"]


class SendLocationSerializer(ModelSerializerCustom):
    class Meta:
        model = SendLocation
        exclude = ["component_type", "bot"]


class SendVenueSerializer(ModelSerializerCustom):
    class Meta:
        model = SendVenue
        exclude = ["component_type", "bot"]


class SendContactSerializer(ModelSerializerCustom):
    class Meta:
        model = SendContact
        exclude = ["component_type", "bot"]


class SendPollSerializer(ModelSerializerCustom):
    class Meta:
        model = SendPoll
        exclude = ["component_type", "bot"]


class SendDiceSerializer(ModelSerializerCustom):
    class Meta:
        model = SendDice
        exclude = ["component_type", "bot"]


class SetMessageReactionSerializer(ModelSerializerCustom):
    class Meta:
        model = SetMessageReaction
        exclude = ["component_type", "bot"]


class GetUserProfilePhotosSerializer(ModelSerializerCustom):
    class Meta:
        model = GetUserProfilePhotos
        exclude = ["component_type", "bot"]


class SetUserEmojiStatusSerializer(ModelSerializerCustom):
    class Meta:
        model = SetUserEmojiStatus
        exclude = ["component_type", "bot"]


class GetFileSerializer(ModelSerializerCustom):
    class Meta:
        model = GetFile
        exclude = ["component_type", "bot"]


class BanChatMemberSerializer(ModelSerializerCustom):
    class Meta:
        model = BanChatMember
        exclude = ["component_type", "bot"]


class UnbanChatMemberSerializer(ModelSerializerCustom):
    class Meta:
        model = UnbanChatMember
        exclude = ["component_type", "bot"]


class RestrictChatMemberSerializer(ModelSerializerCustom):
    class Meta:
        model = RestrictChatMember
        exclude = ["component_type", "bot"]


class PromoteChatMemberSerializer(ModelSerializerCustom):
    class Meta:
        model = PromoteChatMember
        exclude = ["component_type", "bot"]


class SetChatAdministratorCustomTitleSerializer(ModelSerializerCustom):
    class Meta:
        model = SetChatAdministratorCustomTitle
        exclude = ["component_type", "bot"]


class BanChatSenderChatSerializer(ModelSerializerCustom):
    class Meta:
        model = BanChatSenderChat
        exclude = ["component_type", "bot"]


class UnbanChatSenderChatSerializer(ModelSerializerCustom):
    class Meta:
        model = UnbanChatSenderChat
        exclude = ["component_type", "bot"]


class SetChatPermissionsSerializer(ModelSerializerCustom):
    class Meta:
        model = SetChatPermissions
        exclude = ["component_type", "bot"]


class ExportChatInviteLinkSerializer(ModelSerializerCustom):
    class Meta:
        model = ExportChatInviteLink
        exclude = ["component_type", "bot"]


class CreateChatInviteLinkSerializer(ModelSerializerCustom):
    class Meta:
        model = CreateChatInviteLink
        exclude = ["component_type", "bot"]


class EditChatInviteLinkSerializer(ModelSerializerCustom):
    class Meta:
        model = EditChatInviteLink
        exclude = ["component_type", "bot"]


class CreateChatSubscriptionInviteLinkSerializer(ModelSerializerCustom):
    class Meta:
        model = CreateChatSubscriptionInviteLink
        exclude = ["component_type", "bot"]


class EditChatSubscriptionInviteLinkSerializer(ModelSerializerCustom):
    class Meta:
        model = EditChatSubscriptionInviteLink
        exclude = ["component_type", "bot"]


class RevokeChatInviteLinkSerializer(ModelSerializerCustom):
    class Meta:
        model = RevokeChatInviteLink
        exclude = ["component_type", "bot"]


class ApproveChatJoinRequestSerializer(ModelSerializerCustom):
    class Meta:
        model = ApproveChatJoinRequest
        exclude = ["component_type", "bot"]


class DeclineChatJoinRequestSerializer(ModelSerializerCustom):
    class Meta:
        model = DeclineChatJoinRequest
        exclude = ["component_type", "bot"]


class SetChatPhotoSerializer(ModelSerializerCustom):
    class Meta:
        model = SetChatPhoto
        exclude = ["component_type", "bot"]


class DeleteChatPhotoSerializer(ModelSerializerCustom):
    class Meta:
        model = DeleteChatPhoto
        exclude = ["component_type", "bot"]


class SetChatTitleSerializer(ModelSerializerCustom):
    class Meta:
        model = SetChatTitle
        exclude = ["component_type", "bot"]


class SetChatDescriptionSerializer(ModelSerializerCustom):
    class Meta:
        model = SetChatDescription
        exclude = ["component_type", "bot"]


class PinChatMessageSerializer(ModelSerializerCustom):
    class Meta:
        model = PinChatMessage
        exclude = ["component_type", "bot"]


class UnpinChatMessageSerializer(ModelSerializerCustom):
    class Meta:
        model = UnpinChatMessage
        exclude = ["component_type", "bot"]


class UnpinAllChatMessagesSerializer(ModelSerializerCustom):
    class Meta:
        model = UnpinAllChatMessages
        exclude = ["component_type", "bot"]


class LeaveChatSerializer(ModelSerializerCustom):
    class Meta:
        model = LeaveChat
        exclude = ["component_type", "bot"]


class GetChatSerializer(ModelSerializerCustom):
    class Meta:
        model = GetChat
        exclude = ["component_type", "bot"]


class GetChatAdministratorsSerializer(ModelSerializerCustom):
    class Meta:
        model = GetChatAdministrators
        exclude = ["component_type", "bot"]


class GetChatMemberCountSerializer(ModelSerializerCustom):
    class Meta:
        model = GetChatMemberCount
        exclude = ["component_type", "bot"]


class GetChatMemberSerializer(ModelSerializerCustom):
    class Meta:
        model = GetChatMember
        exclude = ["component_type", "bot"]


class SetChatStickerSetSerializer(ModelSerializerCustom):
    class Meta:
        model = SetChatStickerSet
        exclude = ["component_type", "bot"]


class DeleteChatStickerSetSerializer(ModelSerializerCustom):
    class Meta:
        model = DeleteChatStickerSet
        exclude = ["component_type", "bot"]


class CreateForumTopicSerializer(ModelSerializerCustom):
    class Meta:
        model = CreateForumTopic
        exclude = ["component_type", "bot"]


class EditForumTopicSerializer(ModelSerializerCustom):
    class Meta:
        model = EditForumTopic
        exclude = ["component_type", "bot"]


class CloseForumTopicSerializer(ModelSerializerCustom):
    class Meta:
        model = CloseForumTopic
        exclude = ["component_type", "bot"]


class ReopenForumTopicSerializer(ModelSerializerCustom):
    class Meta:
        model = ReopenForumTopic
        exclude = ["component_type", "bot"]


class DeleteForumTopicSerializer(ModelSerializerCustom):
    class Meta:
        model = DeleteForumTopic
        exclude = ["component_type", "bot"]


class UnpinAllForumTopicMessagesSerializer(ModelSerializerCustom):
    class Meta:
        model = UnpinAllForumTopicMessages
        exclude = ["component_type", "bot"]


class EditGeneralForumTopicSerializer(ModelSerializerCustom):
    class Meta:
        model = EditGeneralForumTopic
        exclude = ["component_type", "bot"]


class CloseGeneralForumTopicSerializer(ModelSerializerCustom):
    class Meta:
        model = CloseGeneralForumTopic
        exclude = ["component_type", "bot"]


class ReopenGeneralForumTopicSerializer(ModelSerializerCustom):
    class Meta:
        model = ReopenGeneralForumTopic
        exclude = ["component_type", "bot"]


class HideGeneralForumTopicSerializer(ModelSerializerCustom):
    class Meta:
        model = HideGeneralForumTopic
        exclude = ["component_type", "bot"]


class UnhideGeneralForumTopicSerializer(ModelSerializerCustom):
    class Meta:
        model = UnhideGeneralForumTopic
        exclude = ["component_type", "bot"]


class UnpinAllGeneralForumTopicMessagesSerializer(ModelSerializerCustom):
    class Meta:
        model = UnpinAllGeneralForumTopicMessages
        exclude = ["component_type", "bot"]


class GetUserChatBoostsSerializer(ModelSerializerCustom):
    class Meta:
        model = GetUserChatBoosts
        exclude = ["component_type", "bot"]


class GetBusinessConnectionSerializer(ModelSerializerCustom):
    class Meta:
        model = GetBusinessConnection
        exclude = ["component_type", "bot"]


class SetMyCommandsSerializer(ModelSerializerCustom):
    class Meta:
        model = SetMyCommands
        exclude = ["component_type", "bot"]


class DeleteMyCommandsSerializer(ModelSerializerCustom):
    class Meta:
        model = DeleteMyCommands
        exclude = ["component_type", "bot"]


class GetMyCommandsSerializer(ModelSerializerCustom):
    class Meta:
        model = GetMyCommands
        exclude = ["component_type", "bot"]


class SetMyNameSerializer(ModelSerializerCustom):
    class Meta:
        model = SetMyName
        exclude = ["component_type", "bot"]


class GetMyNameSerializer(ModelSerializerCustom):
    class Meta:
        model = GetMyName
        exclude = ["component_type", "bot"]


class SetMyDescriptionSerializer(ModelSerializerCustom):
    class Meta:
        model = SetMyDescription
        exclude = ["component_type", "bot"]


class GetMyDescriptionSerializer(ModelSerializerCustom):
    class Meta:
        model = GetMyDescription
        exclude = ["component_type", "bot"]


class SetMyShortDescriptionSerializer(ModelSerializerCustom):
    class Meta:
        model = SetMyShortDescription
        exclude = ["component_type", "bot"]


class GetMyShortDescriptionSerializer(ModelSerializerCustom):
    class Meta:
        model = GetMyShortDescription
        exclude = ["component_type", "bot"]


class SetChatMenuButtonSerializer(ModelSerializerCustom):
    class Meta:
        model = SetChatMenuButton
        exclude = ["component_type", "bot"]


class GetChatMenuButtonSerializer(ModelSerializerCustom):
    class Meta:
        model = GetChatMenuButton
        exclude = ["component_type", "bot"]


class SetMyDefaultAdministratorRightsSerializer(ModelSerializerCustom):
    class Meta:
        model = SetMyDefaultAdministratorRights
        exclude = ["component_type", "bot"]


class GetMyDefaultAdministratorRightsSerializer(ModelSerializerCustom):
    class Meta:
        model = GetMyDefaultAdministratorRights
        exclude = ["component_type", "bot"]


class EditMessageTextSerializer(ModelSerializerCustom):
    class Meta:
        model = EditMessageText
        exclude = ["component_type", "bot"]


class EditMessageCaptionSerializer(ModelSerializerCustom):
    class Meta:
        model = EditMessageCaption
        exclude = ["component_type", "bot"]


class EditMessageMediaSerializer(ModelSerializerCustom):
    class Meta:
        model = EditMessageMedia
        exclude = ["component_type", "bot"]


class EditMessageLiveLocationSerializer(ModelSerializerCustom):
    class Meta:
        model = EditMessageLiveLocation
        exclude = ["component_type", "bot"]


class StopMessageLiveLocationSerializer(ModelSerializerCustom):
    class Meta:
        model = StopMessageLiveLocation
        exclude = ["component_type", "bot"]


class EditMessageReplyMarkupSerializer(ModelSerializerCustom):
    class Meta:
        model = EditMessageReplyMarkup
        exclude = ["component_type", "bot"]


class StopPollSerializer(ModelSerializerCustom):
    class Meta:
        model = StopPoll
        exclude = ["component_type", "bot"]


class DeleteMessageSerializer(ModelSerializerCustom):
    class Meta:
        model = DeleteMessage
        exclude = ["component_type", "bot"]


class DeleteMessagesSerializer(ModelSerializerCustom):
    class Meta:
        model = DeleteMessages
        exclude = ["component_type", "bot"]


class SendGiftSerializer(ModelSerializerCustom):
    class Meta:
        model = SendGift
        exclude = ["component_type", "bot"]


class GiftPremiumSubscriptionSerializer(ModelSerializerCustom):
    class Meta:
        model = GiftPremiumSubscription
        exclude = ["component_type", "bot"]


class VerifyUserSerializer(ModelSerializerCustom):
    class Meta:
        model = VerifyUser
        exclude = ["component_type", "bot"]


class VerifyChatSerializer(ModelSerializerCustom):
    class Meta:
        model = VerifyChat
        exclude = ["component_type", "bot"]


class RemoveUserVerificationSerializer(ModelSerializerCustom):
    class Meta:
        model = RemoveUserVerification
        exclude = ["component_type", "bot"]


class RemoveChatVerificationSerializer(ModelSerializerCustom):
    class Meta:
        model = RemoveChatVerification
        exclude = ["component_type", "bot"]


class ReadBusinessMessageSerializer(ModelSerializerCustom):
    class Meta:
        model = ReadBusinessMessage
        exclude = ["component_type", "bot"]


class DeleteBusinessMessagesSerializer(ModelSerializerCustom):
    class Meta:
        model = DeleteBusinessMessages
        exclude = ["component_type", "bot"]


class SetBusinessAccountNameSerializer(ModelSerializerCustom):
    class Meta:
        model = SetBusinessAccountName
        exclude = ["component_type", "bot"]


class SetBusinessAccountUsernameSerializer(ModelSerializerCustom):
    class Meta:
        model = SetBusinessAccountUsername
        exclude = ["component_type", "bot"]


class SetBusinessAccountBioSerializer(ModelSerializerCustom):
    class Meta:
        model = SetBusinessAccountBio
        exclude = ["component_type", "bot"]


class SetBusinessAccountProfilePhotoSerializer(ModelSerializerCustom):
    class Meta:
        model = SetBusinessAccountProfilePhoto
        exclude = ["component_type", "bot"]


class RemoveBusinessAccountProfilePhotoSerializer(ModelSerializerCustom):
    class Meta:
        model = RemoveBusinessAccountProfilePhoto
        exclude = ["component_type", "bot"]


class SetBusinessAccountGiftSettingsSerializer(ModelSerializerCustom):
    class Meta:
        model = SetBusinessAccountGiftSettings
        exclude = ["component_type", "bot"]


class GetBusinessAccountStarBalanceSerializer(ModelSerializerCustom):
    class Meta:
        model = GetBusinessAccountStarBalance
        exclude = ["component_type", "bot"]


class TransferBusinessAccountStarsSerializer(ModelSerializerCustom):
    class Meta:
        model = TransferBusinessAccountStars
        exclude = ["component_type", "bot"]


class GetBusinessAccountGiftsSerializer(ModelSerializerCustom):
    class Meta:
        model = GetBusinessAccountGifts
        exclude = ["component_type", "bot"]


class ConvertGiftToStarsSerializer(ModelSerializerCustom):
    class Meta:
        model = ConvertGiftToStars
        exclude = ["component_type", "bot"]


class UpgradeGiftSerializer(ModelSerializerCustom):
    class Meta:
        model = UpgradeGift
        exclude = ["component_type", "bot"]


class TransferGiftSerializer(ModelSerializerCustom):
    class Meta:
        model = TransferGift
        exclude = ["component_type", "bot"]


class PostStorySerializer(ModelSerializerCustom):
    class Meta:
        model = PostStory
        exclude = ["component_type", "bot"]


class EditStorySerializer(ModelSerializerCustom):
    class Meta:
        model = EditStory
        exclude = ["component_type", "bot"]


class DeleteStorySerializer(ModelSerializerCustom):
    class Meta:
        model = DeleteStory
        exclude = ["component_type", "bot"]


class SendStickerSerializer(ModelSerializerCustom):
    class Meta:
        model = SendSticker
        exclude = ["component_type", "bot"]


class GetStickerSetSerializer(ModelSerializerCustom):
    class Meta:
        model = GetStickerSet
        exclude = ["component_type", "bot"]


class GetCustomEmojiStickersSerializer(ModelSerializerCustom):
    class Meta:
        model = GetCustomEmojiStickers
        exclude = ["component_type", "bot"]


class UploadStickerFileSerializer(ModelSerializerCustom):
    class Meta:
        model = UploadStickerFile
        exclude = ["component_type", "bot"]


class CreateNewStickerSetSerializer(ModelSerializerCustom):
    class Meta:
        model = CreateNewStickerSet
        exclude = ["component_type", "bot"]


class AddStickerToSetSerializer(ModelSerializerCustom):
    class Meta:
        model = AddStickerToSet
        exclude = ["component_type", "bot"]


class SetStickerPositionInSetSerializer(ModelSerializerCustom):
    class Meta:
        model = SetStickerPositionInSet
        exclude = ["component_type", "bot"]


class DeleteStickerFromSetSerializer(ModelSerializerCustom):
    class Meta:
        model = DeleteStickerFromSet
        exclude = ["component_type", "bot"]


class ReplaceStickerInSetSerializer(ModelSerializerCustom):
    class Meta:
        model = ReplaceStickerInSet
        exclude = ["component_type", "bot"]


class SetStickerEmojiListSerializer(ModelSerializerCustom):
    class Meta:
        model = SetStickerEmojiList
        exclude = ["component_type", "bot"]


class SetStickerKeywordsSerializer(ModelSerializerCustom):
    class Meta:
        model = SetStickerKeywords
        exclude = ["component_type", "bot"]


class SetStickerMaskPositionSerializer(ModelSerializerCustom):
    class Meta:
        model = SetStickerMaskPosition
        exclude = ["component_type", "bot"]


class SetStickerSetTitleSerializer(ModelSerializerCustom):
    class Meta:
        model = SetStickerSetTitle
        exclude = ["component_type", "bot"]


class SetStickerSetThumbnailSerializer(ModelSerializerCustom):
    class Meta:
        model = SetStickerSetThumbnail
        exclude = ["component_type", "bot"]


class SetCustomEmojiStickerSetThumbnailSerializer(ModelSerializerCustom):
    class Meta:
        model = SetCustomEmojiStickerSetThumbnail
        exclude = ["component_type", "bot"]


class DeleteStickerSetSerializer(ModelSerializerCustom):
    class Meta:
        model = DeleteStickerSet
        exclude = ["component_type", "bot"]


class AnswerInlineQuerySerializer(ModelSerializerCustom):
    class Meta:
        model = AnswerInlineQuery
        exclude = ["component_type", "bot"]


class AnswerWebAppQuerySerializer(ModelSerializerCustom):
    class Meta:
        model = AnswerWebAppQuery
        exclude = ["component_type", "bot"]


class SavePreparedInlineMessageSerializer(ModelSerializerCustom):
    class Meta:
        model = SavePreparedInlineMessage
        exclude = ["component_type", "bot"]


class SendInvoiceSerializer(ModelSerializerCustom):
    class Meta:
        model = SendInvoice
        exclude = ["component_type", "bot"]


class CreateInvoiceLinkSerializer(ModelSerializerCustom):
    class Meta:
        model = CreateInvoiceLink
        exclude = ["component_type", "bot"]


class AnswerShippingQuerySerializer(ModelSerializerCustom):
    class Meta:
        model = AnswerShippingQuery
        exclude = ["component_type", "bot"]


class AnswerPreCheckoutQuerySerializer(ModelSerializerCustom):
    class Meta:
        model = AnswerPreCheckoutQuery
        exclude = ["component_type", "bot"]


class GetStarTransactionsSerializer(ModelSerializerCustom):
    class Meta:
        model = GetStarTransactions
        exclude = ["component_type", "bot"]


class RefundStarPaymentSerializer(ModelSerializerCustom):
    class Meta:
        model = RefundStarPayment
        exclude = ["component_type", "bot"]


class EditUserStarSubscriptionSerializer(ModelSerializerCustom):
    class Meta:
        model = EditUserStarSubscription
        exclude = ["component_type", "bot"]


class SendGameSerializer(ModelSerializerCustom):
    class Meta:
        model = SendGame
        exclude = ["component_type", "bot"]


class SetGameScoreSerializer(ModelSerializerCustom):
    class Meta:
        model = SetGameScore
        exclude = ["component_type", "bot"]
