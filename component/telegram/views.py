from django.db.models import QuerySet
from rest_framework.viewsets import ModelViewSet

from bot.permissions import IsBotOwner
from component.telegram.serializers import *
from iam.permissions import IsLoginedPermission


class ModelViewSetCustom(ModelViewSet):
    def get_serializer_context(self) -> dict:
        context = super().get_serializer_context()
        context["bot"] = self.kwargs.get("bot")
        return context

    def get_queryset(self) -> QuerySet:
        return self.get_queryset().filter(bot=self.kwargs.get("bot"))


class SendMessageViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SendMessageSerializer
    queryset = SendMessage.objects.all()


class ForwardMessageViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = ForwardMessageSerializer
    queryset = ForwardMessage.objects.all()


class ForwardMessagesViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = ForwardMessagesSerializer
    queryset = ForwardMessages.objects.all()


class CopyMessageViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = CopyMessageSerializer
    queryset = CopyMessage.objects.all()


class CopyMessagesViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = CopyMessagesSerializer
    queryset = CopyMessages.objects.all()


class SendPhotoViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SendPhotoSerializer
    queryset = SendPhoto.objects.all()


class SendDocumentViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SendDocumentSerializer
    queryset = SendDocument.objects.all()


class SendVideoViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SendVideoSerializer
    queryset = SendVideo.objects.all()


class SendAnimationViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SendAnimationSerializer
    queryset = SendAnimation.objects.all()


class SendVoiceViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SendVoiceSerializer
    queryset = SendVoice.objects.all()


class SendVideoNoteViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SendVideoNoteSerializer
    queryset = SendVideoNote.objects.all()


class SendPaidMediaViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SendPaidMediaSerializer
    queryset = SendPaidMedia.objects.all()


class SendMediaGroupViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SendMediaGroupSerializer
    queryset = SendMediaGroup.objects.all()


class SendLocationViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SendLocationSerializer
    queryset = SendLocation.objects.all()


class SendVenueViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SendVenueSerializer
    queryset = SendVenue.objects.all()


class SendContactViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SendContactSerializer
    queryset = SendContact.objects.all()


class SendPollViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SendPollSerializer
    queryset = SendPoll.objects.all()


class SendDiceViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SendDiceSerializer
    queryset = SendDice.objects.all()


class SetMessageReactionViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SetMessageReactionSerializer
    queryset = SetMessageReaction.objects.all()


class GetUserProfilePhotosViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = GetUserProfilePhotosSerializer
    queryset = GetUserProfilePhotos.objects.all()


class SetUserEmojiStatusViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SetUserEmojiStatusSerializer
    queryset = SetUserEmojiStatus.objects.all()


class GetFileViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = GetFileSerializer
    queryset = GetFile.objects.all()


class BanChatMemberViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = BanChatMemberSerializer
    queryset = BanChatMember.objects.all()


class UnbanChatMemberViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = UnbanChatMemberSerializer
    queryset = UnbanChatMember.objects.all()


class RestrictChatMemberViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = RestrictChatMemberSerializer
    queryset = RestrictChatMember.objects.all()


class PromoteChatMemberViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = PromoteChatMemberSerializer
    queryset = PromoteChatMember.objects.all()


class SetChatAdministratorCustomTitleViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SetChatAdministratorCustomTitleSerializer
    queryset = SetChatAdministratorCustomTitle.objects.all()


class BanChatSenderChatViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = BanChatSenderChatSerializer
    queryset = BanChatSenderChat.objects.all()


class UnbanChatSenderChatViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = UnbanChatSenderChatSerializer
    queryset = UnbanChatSenderChat.objects.all()


class SetChatPermissionsViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SetChatPermissionsSerializer
    queryset = SetChatPermissions.objects.all()


class ExportChatInviteLinkViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = ExportChatInviteLinkSerializer
    queryset = ExportChatInviteLink.objects.all()


class CreateChatInviteLinkViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = CreateChatInviteLinkSerializer
    queryset = CreateChatInviteLink.objects.all()


class EditChatInviteLinkViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = EditChatInviteLinkSerializer
    queryset = EditChatInviteLink.objects.all()


class CreateChatSubscriptionInviteLinkViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = CreateChatSubscriptionInviteLinkSerializer
    queryset = CreateChatSubscriptionInviteLink.objects.all()


class EditChatSubscriptionInviteLinkViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = EditChatSubscriptionInviteLinkSerializer
    queryset = EditChatSubscriptionInviteLink.objects.all()


class RevokeChatInviteLinkViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = RevokeChatInviteLinkSerializer
    queryset = RevokeChatInviteLink.objects.all()


class ApproveChatJoinRequestViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = ApproveChatJoinRequestSerializer
    queryset = ApproveChatJoinRequest.objects.all()


class DeclineChatJoinRequestViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = DeclineChatJoinRequestSerializer
    queryset = DeclineChatJoinRequest.objects.all()


class SetChatPhotoViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SetChatPhotoSerializer
    queryset = SetChatPhoto.objects.all()


class DeleteChatPhotoViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = DeleteChatPhotoSerializer
    queryset = DeleteChatPhoto.objects.all()


class SetChatTitleViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SetChatTitleSerializer
    queryset = SetChatTitle.objects.all()


class SetChatDescriptionViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SetChatDescriptionSerializer
    queryset = SetChatDescription.objects.all()


class PinChatMessageViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = PinChatMessageSerializer
    queryset = PinChatMessage.objects.all()


class UnpinChatMessageViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = UnpinChatMessageSerializer
    queryset = UnpinChatMessage.objects.all()


class UnpinAllChatMessagesViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = UnpinAllChatMessagesSerializer
    queryset = UnpinAllChatMessages.objects.all()


class LeaveChatViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = LeaveChatSerializer
    queryset = LeaveChat.objects.all()


class GetChatViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = GetChatSerializer
    queryset = GetChat.objects.all()


class GetChatAdministratorsViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = GetChatAdministratorsSerializer
    queryset = GetChatAdministrators.objects.all()


class GetChatMemberCountViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = GetChatMemberCountSerializer
    queryset = GetChatMemberCount.objects.all()


class GetChatMemberViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = GetChatMemberSerializer
    queryset = GetChatMember.objects.all()


class SetChatStickerSetViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SetChatStickerSetSerializer
    queryset = SetChatStickerSet.objects.all()


class DeleteChatStickerSetViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = DeleteChatStickerSetSerializer
    queryset = DeleteChatStickerSet.objects.all()


class CreateForumTopicViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = CreateForumTopicSerializer
    queryset = CreateForumTopic.objects.all()


class EditForumTopicViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = EditForumTopicSerializer
    queryset = EditForumTopic.objects.all()


class CloseForumTopicViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = CloseForumTopicSerializer
    queryset = CloseForumTopic.objects.all()


class ReopenForumTopicViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = ReopenForumTopicSerializer
    queryset = ReopenForumTopic.objects.all()


class DeleteForumTopicViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = DeleteForumTopicSerializer
    queryset = DeleteForumTopic.objects.all()


class UnpinAllForumTopicMessagesViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = UnpinAllForumTopicMessagesSerializer
    queryset = UnpinAllForumTopicMessages.objects.all()


class EditGeneralForumTopicViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = EditGeneralForumTopicSerializer
    queryset = EditGeneralForumTopic.objects.all()


class CloseGeneralForumTopicViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = CloseGeneralForumTopicSerializer
    queryset = CloseGeneralForumTopic.objects.all()


class ReopenGeneralForumTopicViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = ReopenGeneralForumTopicSerializer
    queryset = ReopenGeneralForumTopic.objects.all()


class HideGeneralForumTopicViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = HideGeneralForumTopicSerializer
    queryset = HideGeneralForumTopic.objects.all()


class UnhideGeneralForumTopicViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = UnhideGeneralForumTopicSerializer
    queryset = UnhideGeneralForumTopic.objects.all()


class UnpinAllGeneralForumTopicMessagesViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = UnpinAllGeneralForumTopicMessagesSerializer
    queryset = UnpinAllGeneralForumTopicMessages.objects.all()


class GetUserChatBoostsViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = GetUserChatBoostsSerializer
    queryset = GetUserChatBoosts.objects.all()


class GetBusinessConnectionViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = GetBusinessConnectionSerializer
    queryset = GetBusinessConnection.objects.all()


class SetMyCommandsViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SetMyCommandsSerializer
    queryset = SetMyCommands.objects.all()


class DeleteMyCommandsViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = DeleteMyCommandsSerializer
    queryset = DeleteMyCommands.objects.all()


class GetMyCommandsViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = GetMyCommandsSerializer
    queryset = GetMyCommands.objects.all()


class SetMyNameViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SetMyNameSerializer
    queryset = SetMyName.objects.all()


class GetMyNameViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = GetMyNameSerializer
    queryset = GetMyName.objects.all()


class SetMyDescriptionViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SetMyDescriptionSerializer
    queryset = SetMyDescription.objects.all()


class GetMyDescriptionViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = GetMyDescriptionSerializer
    queryset = GetMyDescription.objects.all()


class SetMyShortDescriptionViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SetMyShortDescriptionSerializer
    queryset = SetMyShortDescription.objects.all()


class GetMyShortDescriptionViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = GetMyShortDescriptionSerializer
    queryset = GetMyShortDescription.objects.all()


class SetChatMenuButtonViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SetChatMenuButtonSerializer
    queryset = SetChatMenuButton.objects.all()


class GetChatMenuButtonViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = GetChatMenuButtonSerializer
    queryset = GetChatMenuButton.objects.all()


class SetMyDefaultAdministratorRightsViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SetMyDefaultAdministratorRightsSerializer
    queryset = SetMyDefaultAdministratorRights.objects.all()


class GetMyDefaultAdministratorRightsViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = GetMyDefaultAdministratorRightsSerializer
    queryset = GetMyDefaultAdministratorRights.objects.all()


class EditMessageTextViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = EditMessageTextSerializer
    queryset = EditMessageText.objects.all()


class EditMessageCaptionViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = EditMessageCaptionSerializer
    queryset = EditMessageCaption.objects.all()


class EditMessageMediaViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = EditMessageMediaSerializer
    queryset = EditMessageMedia.objects.all()


class EditMessageLiveLocationViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = EditMessageLiveLocationSerializer
    queryset = EditMessageLiveLocation.objects.all()


class StopMessageLiveLocationViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = StopMessageLiveLocationSerializer
    queryset = StopMessageLiveLocation.objects.all()


class EditMessageReplyMarkupViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = EditMessageReplyMarkupSerializer
    queryset = EditMessageReplyMarkup.objects.all()


class StopPollViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = StopPollSerializer
    queryset = StopPoll.objects.all()


class DeleteMessageViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = DeleteMessageSerializer
    queryset = DeleteMessage.objects.all()


class DeleteMessagesViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = DeleteMessagesSerializer
    queryset = DeleteMessages.objects.all()


class SendGiftViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SendGiftSerializer
    queryset = SendGift.objects.all()


class GiftPremiumSubscriptionViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = GiftPremiumSubscriptionSerializer
    queryset = GiftPremiumSubscription.objects.all()


class VerifyUserViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = VerifyUserSerializer
    queryset = VerifyUser.objects.all()


class VerifyChatViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = VerifyChatSerializer
    queryset = VerifyChat.objects.all()


class RemoveUserVerificationViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = RemoveUserVerificationSerializer
    queryset = RemoveUserVerification.objects.all()


class RemoveChatVerificationViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = RemoveChatVerificationSerializer
    queryset = RemoveChatVerification.objects.all()


class ReadBusinessMessageViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = ReadBusinessMessageSerializer
    queryset = ReadBusinessMessage.objects.all()


class DeleteBusinessMessagesViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = DeleteBusinessMessagesSerializer
    queryset = DeleteBusinessMessages.objects.all()


class SetBusinessAccountNameViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SetBusinessAccountNameSerializer
    queryset = SetBusinessAccountName.objects.all()


class SetBusinessAccountUsernameViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SetBusinessAccountUsernameSerializer
    queryset = SetBusinessAccountUsername.objects.all()


class SetBusinessAccountBioViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SetBusinessAccountBioSerializer
    queryset = SetBusinessAccountBio.objects.all()


class SetBusinessAccountProfilePhotoViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SetBusinessAccountProfilePhotoSerializer
    queryset = SetBusinessAccountProfilePhoto.objects.all()


class RemoveBusinessAccountProfilePhotoViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = RemoveBusinessAccountProfilePhotoSerializer
    queryset = RemoveBusinessAccountProfilePhoto.objects.all()


class SetBusinessAccountGiftSettingsViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SetBusinessAccountGiftSettingsSerializer
    queryset = SetBusinessAccountGiftSettings.objects.all()


class GetBusinessAccountStarBalanceViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = GetBusinessAccountStarBalanceSerializer
    queryset = GetBusinessAccountStarBalance.objects.all()


class TransferBusinessAccountStarsViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = TransferBusinessAccountStarsSerializer
    queryset = TransferBusinessAccountStars.objects.all()


class GetBusinessAccountGiftsViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = GetBusinessAccountGiftsSerializer
    queryset = GetBusinessAccountGifts.objects.all()


class ConvertGiftToStarsViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = ConvertGiftToStarsSerializer
    queryset = ConvertGiftToStars.objects.all()


class UpgradeGiftViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = UpgradeGiftSerializer
    queryset = UpgradeGift.objects.all()


class TransferGiftViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = TransferGiftSerializer
    queryset = TransferGift.objects.all()


class PostStoryViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = PostStorySerializer
    queryset = PostStory.objects.all()


class EditStoryViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = EditStorySerializer
    queryset = EditStory.objects.all()


class DeleteStoryViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = DeleteStorySerializer
    queryset = DeleteStory.objects.all()


class SendStickerViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SendStickerSerializer
    queryset = SendSticker.objects.all()


class GetStickerSetViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = GetStickerSetSerializer
    queryset = GetStickerSet.objects.all()


class GetCustomEmojiStickersViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = GetCustomEmojiStickersSerializer
    queryset = GetCustomEmojiStickers.objects.all()


class UploadStickerFileViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = UploadStickerFileSerializer
    queryset = UploadStickerFile.objects.all()


class CreateNewStickerSetViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = CreateNewStickerSetSerializer
    queryset = CreateNewStickerSet.objects.all()


class AddStickerToSetViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = AddStickerToSetSerializer
    queryset = AddStickerToSet.objects.all()


class SetStickerPositionInSetViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SetStickerPositionInSetSerializer
    queryset = SetStickerPositionInSet.objects.all()


class DeleteStickerFromSetViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = DeleteStickerFromSetSerializer
    queryset = DeleteStickerFromSet.objects.all()


class ReplaceStickerInSetViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = ReplaceStickerInSetSerializer
    queryset = ReplaceStickerInSet.objects.all()


class SetStickerEmojiListViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SetStickerEmojiListSerializer
    queryset = SetStickerEmojiList.objects.all()


class SetStickerKeywordsViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SetStickerKeywordsSerializer
    queryset = SetStickerKeywords.objects.all()


class SetStickerMaskPositionViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SetStickerMaskPositionSerializer
    queryset = SetStickerMaskPosition.objects.all()


class SetStickerSetTitleViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SetStickerSetTitleSerializer
    queryset = SetStickerSetTitle.objects.all()


class SetStickerSetThumbnailViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SetStickerSetThumbnailSerializer
    queryset = SetStickerSetThumbnail.objects.all()


class SetCustomEmojiStickerSetThumbnailViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SetCustomEmojiStickerSetThumbnailSerializer
    queryset = SetCustomEmojiStickerSetThumbnail.objects.all()


class DeleteStickerSetViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = DeleteStickerSetSerializer
    queryset = DeleteStickerSet.objects.all()


class AnswerInlineQueryViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = AnswerInlineQuerySerializer
    queryset = AnswerInlineQuery.objects.all()


class AnswerWebAppQueryViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = AnswerWebAppQuerySerializer
    queryset = AnswerWebAppQuery.objects.all()


class SavePreparedInlineMessageViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SavePreparedInlineMessageSerializer
    queryset = SavePreparedInlineMessage.objects.all()


class SendInvoiceViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SendInvoiceSerializer
    queryset = SendInvoice.objects.all()


class CreateInvoiceLinkViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = CreateInvoiceLinkSerializer
    queryset = CreateInvoiceLink.objects.all()


class AnswerShippingQueryViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = AnswerShippingQuerySerializer
    queryset = AnswerShippingQuery.objects.all()


class AnswerPreCheckoutQueryViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = AnswerPreCheckoutQuerySerializer
    queryset = AnswerPreCheckoutQuery.objects.all()


class GetStarTransactionsViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = GetStarTransactionsSerializer
    queryset = GetStarTransactions.objects.all()


class RefundStarPaymentViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = RefundStarPaymentSerializer
    queryset = RefundStarPayment.objects.all()


class EditUserStarSubscriptionViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = EditUserStarSubscriptionSerializer
    queryset = EditUserStarSubscription.objects.all()


class SendGameViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SendGameSerializer
    queryset = SendGame.objects.all()


class SetGameScoreViewSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SetGameScoreSerializer
    queryset = SetGameScore.objects.all()
