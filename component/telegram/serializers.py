from rest_framework import serializers

from component.telegram.models import *


class ModelSerializerCustom(serializers.ModelSerializer):
    reply_markup_supported = serializers.SerializerMethodField()

    def create(self, validated_data: dict) -> Component:
        validated_data["bot_id"] = self.context.get("bot")
        return super().create(validated_data)

    def get_reply_markup_supported(self, obj: Component) -> bool:
        model_class = obj.component_content_type.model_class()
        if hasattr(model_class, "reply_markup_supported"):
            return model_class().reply_markup_supported
        return False


class SendMessageSerializer(ModelSerializerCustom):
    class Meta:
        model = SendMessage
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class ForwardMessageSerializer(ModelSerializerCustom):
    class Meta:
        model = ForwardMessage
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class ForwardMessagesSerializer(ModelSerializerCustom):
    class Meta:
        model = ForwardMessages
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class CopyMessageSerializer(ModelSerializerCustom):
    class Meta:
        model = CopyMessage
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class CopyMessagesSerializer(ModelSerializerCustom):
    class Meta:
        model = CopyMessages
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SendPhotoSerializer(ModelSerializerCustom):
    class Meta:
        model = SendPhoto
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SendDocumentSerializer(ModelSerializerCustom):
    class Meta:
        model = SendDocument
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SendVideoSerializer(ModelSerializerCustom):
    class Meta:
        model = SendVideo
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SendAnimationSerializer(ModelSerializerCustom):
    class Meta:
        model = SendAnimation
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SendVoiceSerializer(ModelSerializerCustom):
    class Meta:
        model = SendVoice
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SendVideoNoteSerializer(ModelSerializerCustom):
    class Meta:
        model = SendVideoNote
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SendPaidMediaSerializer(ModelSerializerCustom):
    class Meta:
        model = SendPaidMedia
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SendMediaGroupSerializer(ModelSerializerCustom):
    class Meta:
        model = SendMediaGroup
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SendLocationSerializer(ModelSerializerCustom):
    class Meta:
        model = SendLocation
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SendVenueSerializer(ModelSerializerCustom):
    class Meta:
        model = SendVenue
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SendContactSerializer(ModelSerializerCustom):
    class Meta:
        model = SendContact
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SendPollSerializer(ModelSerializerCustom):
    class Meta:
        model = SendPoll
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SendDiceSerializer(ModelSerializerCustom):
    class Meta:
        model = SendDice
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SetMessageReactionSerializer(ModelSerializerCustom):
    class Meta:
        model = SetMessageReaction
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class GetUserProfilePhotosSerializer(ModelSerializerCustom):
    class Meta:
        model = GetUserProfilePhotos
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SetUserEmojiStatusSerializer(ModelSerializerCustom):
    class Meta:
        model = SetUserEmojiStatus
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class GetFileSerializer(ModelSerializerCustom):
    class Meta:
        model = GetFile
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class BanChatMemberSerializer(ModelSerializerCustom):
    class Meta:
        model = BanChatMember
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class UnbanChatMemberSerializer(ModelSerializerCustom):
    class Meta:
        model = UnbanChatMember
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class RestrictChatMemberSerializer(ModelSerializerCustom):
    class Meta:
        model = RestrictChatMember
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class PromoteChatMemberSerializer(ModelSerializerCustom):
    class Meta:
        model = PromoteChatMember
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SetChatAdministratorCustomTitleSerializer(ModelSerializerCustom):
    class Meta:
        model = SetChatAdministratorCustomTitle
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class BanChatSenderChatSerializer(ModelSerializerCustom):
    class Meta:
        model = BanChatSenderChat
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class UnbanChatSenderChatSerializer(ModelSerializerCustom):
    class Meta:
        model = UnbanChatSenderChat
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SetChatPermissionsSerializer(ModelSerializerCustom):
    class Meta:
        model = SetChatPermissions
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class ExportChatInviteLinkSerializer(ModelSerializerCustom):
    class Meta:
        model = ExportChatInviteLink
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class CreateChatInviteLinkSerializer(ModelSerializerCustom):
    class Meta:
        model = CreateChatInviteLink
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class EditChatInviteLinkSerializer(ModelSerializerCustom):
    class Meta:
        model = EditChatInviteLink
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class CreateChatSubscriptionInviteLinkSerializer(ModelSerializerCustom):
    class Meta:
        model = CreateChatSubscriptionInviteLink
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class EditChatSubscriptionInviteLinkSerializer(ModelSerializerCustom):
    class Meta:
        model = EditChatSubscriptionInviteLink
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class RevokeChatInviteLinkSerializer(ModelSerializerCustom):
    class Meta:
        model = RevokeChatInviteLink
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class ApproveChatJoinRequestSerializer(ModelSerializerCustom):
    class Meta:
        model = ApproveChatJoinRequest
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class DeclineChatJoinRequestSerializer(ModelSerializerCustom):
    class Meta:
        model = DeclineChatJoinRequest
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SetChatPhotoSerializer(ModelSerializerCustom):
    class Meta:
        model = SetChatPhoto
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class DeleteChatPhotoSerializer(ModelSerializerCustom):
    class Meta:
        model = DeleteChatPhoto
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SetChatTitleSerializer(ModelSerializerCustom):
    class Meta:
        model = SetChatTitle
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SetChatDescriptionSerializer(ModelSerializerCustom):
    class Meta:
        model = SetChatDescription
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class PinChatMessageSerializer(ModelSerializerCustom):
    class Meta:
        model = PinChatMessage
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class UnpinChatMessageSerializer(ModelSerializerCustom):
    class Meta:
        model = UnpinChatMessage
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class UnpinAllChatMessagesSerializer(ModelSerializerCustom):
    class Meta:
        model = UnpinAllChatMessages
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class LeaveChatSerializer(ModelSerializerCustom):
    class Meta:
        model = LeaveChat
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class GetChatSerializer(ModelSerializerCustom):
    class Meta:
        model = GetChat
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class GetChatAdministratorsSerializer(ModelSerializerCustom):
    class Meta:
        model = GetChatAdministrators
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class GetChatMemberCountSerializer(ModelSerializerCustom):
    class Meta:
        model = GetChatMemberCount
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class GetChatMemberSerializer(ModelSerializerCustom):
    class Meta:
        model = GetChatMember
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SetChatStickerSetSerializer(ModelSerializerCustom):
    class Meta:
        model = SetChatStickerSet
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class DeleteChatStickerSetSerializer(ModelSerializerCustom):
    class Meta:
        model = DeleteChatStickerSet
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class CreateForumTopicSerializer(ModelSerializerCustom):
    class Meta:
        model = CreateForumTopic
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class EditForumTopicSerializer(ModelSerializerCustom):
    class Meta:
        model = EditForumTopic
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class CloseForumTopicSerializer(ModelSerializerCustom):
    class Meta:
        model = CloseForumTopic
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class ReopenForumTopicSerializer(ModelSerializerCustom):
    class Meta:
        model = ReopenForumTopic
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class DeleteForumTopicSerializer(ModelSerializerCustom):
    class Meta:
        model = DeleteForumTopic
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class UnpinAllForumTopicMessagesSerializer(ModelSerializerCustom):
    class Meta:
        model = UnpinAllForumTopicMessages
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class EditGeneralForumTopicSerializer(ModelSerializerCustom):
    class Meta:
        model = EditGeneralForumTopic
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class CloseGeneralForumTopicSerializer(ModelSerializerCustom):
    class Meta:
        model = CloseGeneralForumTopic
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class ReopenGeneralForumTopicSerializer(ModelSerializerCustom):
    class Meta:
        model = ReopenGeneralForumTopic
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class HideGeneralForumTopicSerializer(ModelSerializerCustom):
    class Meta:
        model = HideGeneralForumTopic
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class UnhideGeneralForumTopicSerializer(ModelSerializerCustom):
    class Meta:
        model = UnhideGeneralForumTopic
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class UnpinAllGeneralForumTopicMessagesSerializer(ModelSerializerCustom):
    class Meta:
        model = UnpinAllGeneralForumTopicMessages
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class GetUserChatBoostsSerializer(ModelSerializerCustom):
    class Meta:
        model = GetUserChatBoosts
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class GetBusinessConnectionSerializer(ModelSerializerCustom):
    class Meta:
        model = GetBusinessConnection
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SetMyCommandsSerializer(ModelSerializerCustom):
    class Meta:
        model = SetMyCommands
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class DeleteMyCommandsSerializer(ModelSerializerCustom):
    class Meta:
        model = DeleteMyCommands
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class GetMyCommandsSerializer(ModelSerializerCustom):
    class Meta:
        model = GetMyCommands
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SetMyNameSerializer(ModelSerializerCustom):
    class Meta:
        model = SetMyName
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class GetMyNameSerializer(ModelSerializerCustom):
    class Meta:
        model = GetMyName
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SetMyDescriptionSerializer(ModelSerializerCustom):
    class Meta:
        model = SetMyDescription
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class GetMyDescriptionSerializer(ModelSerializerCustom):
    class Meta:
        model = GetMyDescription
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SetMyShortDescriptionSerializer(ModelSerializerCustom):
    class Meta:
        model = SetMyShortDescription
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class GetMyShortDescriptionSerializer(ModelSerializerCustom):
    class Meta:
        model = GetMyShortDescription
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SetChatMenuButtonSerializer(ModelSerializerCustom):
    class Meta:
        model = SetChatMenuButton
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class GetChatMenuButtonSerializer(ModelSerializerCustom):
    class Meta:
        model = GetChatMenuButton
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SetMyDefaultAdministratorRightsSerializer(ModelSerializerCustom):
    class Meta:
        model = SetMyDefaultAdministratorRights
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class GetMyDefaultAdministratorRightsSerializer(ModelSerializerCustom):
    class Meta:
        model = GetMyDefaultAdministratorRights
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class EditMessageTextSerializer(ModelSerializerCustom):
    class Meta:
        model = EditMessageText
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class EditMessageCaptionSerializer(ModelSerializerCustom):
    class Meta:
        model = EditMessageCaption
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class EditMessageMediaSerializer(ModelSerializerCustom):
    class Meta:
        model = EditMessageMedia
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class EditMessageLiveLocationSerializer(ModelSerializerCustom):
    class Meta:
        model = EditMessageLiveLocation
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class StopMessageLiveLocationSerializer(ModelSerializerCustom):
    class Meta:
        model = StopMessageLiveLocation
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class EditMessageReplyMarkupSerializer(ModelSerializerCustom):
    class Meta:
        model = EditMessageReplyMarkup
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class StopPollSerializer(ModelSerializerCustom):
    class Meta:
        model = StopPoll
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class DeleteMessageSerializer(ModelSerializerCustom):
    class Meta:
        model = DeleteMessage
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class DeleteMessagesSerializer(ModelSerializerCustom):
    class Meta:
        model = DeleteMessages
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SendGiftSerializer(ModelSerializerCustom):
    class Meta:
        model = SendGift
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class GiftPremiumSubscriptionSerializer(ModelSerializerCustom):
    class Meta:
        model = GiftPremiumSubscription
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class VerifyUserSerializer(ModelSerializerCustom):
    class Meta:
        model = VerifyUser
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class VerifyChatSerializer(ModelSerializerCustom):
    class Meta:
        model = VerifyChat
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class RemoveUserVerificationSerializer(ModelSerializerCustom):
    class Meta:
        model = RemoveUserVerification
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class RemoveChatVerificationSerializer(ModelSerializerCustom):
    class Meta:
        model = RemoveChatVerification
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class ReadBusinessMessageSerializer(ModelSerializerCustom):
    class Meta:
        model = ReadBusinessMessage
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class DeleteBusinessMessagesSerializer(ModelSerializerCustom):
    class Meta:
        model = DeleteBusinessMessages
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SetBusinessAccountNameSerializer(ModelSerializerCustom):
    class Meta:
        model = SetBusinessAccountName
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SetBusinessAccountUsernameSerializer(ModelSerializerCustom):
    class Meta:
        model = SetBusinessAccountUsername
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SetBusinessAccountBioSerializer(ModelSerializerCustom):
    class Meta:
        model = SetBusinessAccountBio
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SetBusinessAccountProfilePhotoSerializer(ModelSerializerCustom):
    class Meta:
        model = SetBusinessAccountProfilePhoto
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class RemoveBusinessAccountProfilePhotoSerializer(ModelSerializerCustom):
    class Meta:
        model = RemoveBusinessAccountProfilePhoto
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SetBusinessAccountGiftSettingsSerializer(ModelSerializerCustom):
    class Meta:
        model = SetBusinessAccountGiftSettings
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class GetBusinessAccountStarBalanceSerializer(ModelSerializerCustom):
    class Meta:
        model = GetBusinessAccountStarBalance
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class TransferBusinessAccountStarsSerializer(ModelSerializerCustom):
    class Meta:
        model = TransferBusinessAccountStars
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class GetBusinessAccountGiftsSerializer(ModelSerializerCustom):
    class Meta:
        model = GetBusinessAccountGifts
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class ConvertGiftToStarsSerializer(ModelSerializerCustom):
    class Meta:
        model = ConvertGiftToStars
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class UpgradeGiftSerializer(ModelSerializerCustom):
    class Meta:
        model = UpgradeGift
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class TransferGiftSerializer(ModelSerializerCustom):
    class Meta:
        model = TransferGift
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class PostStorySerializer(ModelSerializerCustom):
    class Meta:
        model = PostStory
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class EditStorySerializer(ModelSerializerCustom):
    class Meta:
        model = EditStory
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class DeleteStorySerializer(ModelSerializerCustom):
    class Meta:
        model = DeleteStory
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SendStickerSerializer(ModelSerializerCustom):
    class Meta:
        model = SendSticker
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class GetStickerSetSerializer(ModelSerializerCustom):
    class Meta:
        model = GetStickerSet
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class GetCustomEmojiStickersSerializer(ModelSerializerCustom):
    class Meta:
        model = GetCustomEmojiStickers
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class UploadStickerFileSerializer(ModelSerializerCustom):
    class Meta:
        model = UploadStickerFile
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class CreateNewStickerSetSerializer(ModelSerializerCustom):
    class Meta:
        model = CreateNewStickerSet
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class AddStickerToSetSerializer(ModelSerializerCustom):
    class Meta:
        model = AddStickerToSet
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SetStickerPositionInSetSerializer(ModelSerializerCustom):
    class Meta:
        model = SetStickerPositionInSet
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class DeleteStickerFromSetSerializer(ModelSerializerCustom):
    class Meta:
        model = DeleteStickerFromSet
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class ReplaceStickerInSetSerializer(ModelSerializerCustom):
    class Meta:
        model = ReplaceStickerInSet
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SetStickerEmojiListSerializer(ModelSerializerCustom):
    class Meta:
        model = SetStickerEmojiList
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SetStickerKeywordsSerializer(ModelSerializerCustom):
    class Meta:
        model = SetStickerKeywords
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SetStickerMaskPositionSerializer(ModelSerializerCustom):
    class Meta:
        model = SetStickerMaskPosition
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SetStickerSetTitleSerializer(ModelSerializerCustom):
    class Meta:
        model = SetStickerSetTitle
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SetStickerSetThumbnailSerializer(ModelSerializerCustom):
    class Meta:
        model = SetStickerSetThumbnail
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SetCustomEmojiStickerSetThumbnailSerializer(ModelSerializerCustom):
    class Meta:
        model = SetCustomEmojiStickerSetThumbnail
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class DeleteStickerSetSerializer(ModelSerializerCustom):
    class Meta:
        model = DeleteStickerSet
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class AnswerInlineQuerySerializer(ModelSerializerCustom):
    class Meta:
        model = AnswerInlineQuery
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class AnswerWebAppQuerySerializer(ModelSerializerCustom):
    class Meta:
        model = AnswerWebAppQuery
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SavePreparedInlineMessageSerializer(ModelSerializerCustom):
    class Meta:
        model = SavePreparedInlineMessage
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SendInvoiceSerializer(ModelSerializerCustom):
    class Meta:
        model = SendInvoice
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class CreateInvoiceLinkSerializer(ModelSerializerCustom):
    class Meta:
        model = CreateInvoiceLink
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class AnswerShippingQuerySerializer(ModelSerializerCustom):
    class Meta:
        model = AnswerShippingQuery
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class AnswerPreCheckoutQuerySerializer(ModelSerializerCustom):
    class Meta:
        model = AnswerPreCheckoutQuery
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class GetStarTransactionsSerializer(ModelSerializerCustom):
    class Meta:
        model = GetStarTransactions
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class RefundStarPaymentSerializer(ModelSerializerCustom):
    class Meta:
        model = RefundStarPayment
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class EditUserStarSubscriptionSerializer(ModelSerializerCustom):
    class Meta:
        model = EditUserStarSubscription
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SendGameSerializer(ModelSerializerCustom):
    class Meta:
        model = SendGame
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]


class SetGameScoreSerializer(ModelSerializerCustom):
    class Meta:
        model = SetGameScore
        exclude = ["bot"]
        read_only_fields = ["component_type", "reply_markup_supported"]
