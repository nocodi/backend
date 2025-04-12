from rest_framework.viewsets import ModelViewSet

from component.serializers import *


class SendMessageViewSet(ModelViewSet):
    serializer_class = SendMessageSerializer
    queryset = SendMessage.objects.all()


class ForwardMessageViewSet(ModelViewSet):
    serializer_class = ForwardMessageSerializer
    queryset = ForwardMessage.objects.all()


class ForwardMessagesViewSet(ModelViewSet):
    serializer_class = ForwardMessagesSerializer
    queryset = ForwardMessages.objects.all()


class CopyMessageViewSet(ModelViewSet):
    serializer_class = CopyMessageSerializer
    queryset = CopyMessage.objects.all()


class CopyMessagesViewSet(ModelViewSet):
    serializer_class = CopyMessagesSerializer
    queryset = CopyMessages.objects.all()


class SendPhotoViewSet(ModelViewSet):
    serializer_class = SendPhotoSerializer
    queryset = SendPhoto.objects.all()


class SendDocumentViewSet(ModelViewSet):
    serializer_class = SendDocumentSerializer
    queryset = SendDocument.objects.all()


class SendVideoViewSet(ModelViewSet):
    serializer_class = SendVideoSerializer
    queryset = SendVideo.objects.all()


class SendAnimationViewSet(ModelViewSet):
    serializer_class = SendAnimationSerializer
    queryset = SendAnimation.objects.all()


class SendVoiceViewSet(ModelViewSet):
    serializer_class = SendVoiceSerializer
    queryset = SendVoice.objects.all()


class SendVideoNoteViewSet(ModelViewSet):
    serializer_class = SendVideoNoteSerializer
    queryset = SendVideoNote.objects.all()


class SendPaidMediaViewSet(ModelViewSet):
    serializer_class = SendPaidMediaSerializer
    queryset = SendPaidMedia.objects.all()


class SendMediaGroupViewSet(ModelViewSet):
    serializer_class = SendMediaGroupSerializer
    queryset = SendMediaGroup.objects.all()


class SendLocationViewSet(ModelViewSet):
    serializer_class = SendLocationSerializer
    queryset = SendLocation.objects.all()


class SendVenueViewSet(ModelViewSet):
    serializer_class = SendVenueSerializer
    queryset = SendVenue.objects.all()


class SendContactViewSet(ModelViewSet):
    serializer_class = SendContactSerializer
    queryset = SendContact.objects.all()


class SendPollViewSet(ModelViewSet):
    serializer_class = SendPollSerializer
    queryset = SendPoll.objects.all()


class SendDiceViewSet(ModelViewSet):
    serializer_class = SendDiceSerializer
    queryset = SendDice.objects.all()


class SetMessageReactionViewSet(ModelViewSet):
    serializer_class = SetMessageReactionSerializer
    queryset = SetMessageReaction.objects.all()


class GetUserProfilePhotosViewSet(ModelViewSet):
    serializer_class = GetUserProfilePhotosSerializer
    queryset = GetUserProfilePhotos.objects.all()


class SetUserEmojiStatusViewSet(ModelViewSet):
    serializer_class = SetUserEmojiStatusSerializer
    queryset = SetUserEmojiStatus.objects.all()


class GetFileViewSet(ModelViewSet):
    serializer_class = GetFileSerializer
    queryset = GetFile.objects.all()


class BanChatMemberViewSet(ModelViewSet):
    serializer_class = BanChatMemberSerializer
    queryset = BanChatMember.objects.all()


class UnbanChatMemberViewSet(ModelViewSet):
    serializer_class = UnbanChatMemberSerializer
    queryset = UnbanChatMember.objects.all()


class RestrictChatMemberViewSet(ModelViewSet):
    serializer_class = RestrictChatMemberSerializer
    queryset = RestrictChatMember.objects.all()


class PromoteChatMemberViewSet(ModelViewSet):
    serializer_class = PromoteChatMemberSerializer
    queryset = PromoteChatMember.objects.all()


class SetChatAdministratorCustomTitleViewSet(ModelViewSet):
    serializer_class = SetChatAdministratorCustomTitleSerializer
    queryset = SetChatAdministratorCustomTitle.objects.all()


class BanChatSenderChatViewSet(ModelViewSet):
    serializer_class = BanChatSenderChatSerializer
    queryset = BanChatSenderChat.objects.all()


class UnbanChatSenderChatViewSet(ModelViewSet):
    serializer_class = UnbanChatSenderChatSerializer
    queryset = UnbanChatSenderChat.objects.all()


class SetChatPermissionsViewSet(ModelViewSet):
    serializer_class = SetChatPermissionsSerializer
    queryset = SetChatPermissions.objects.all()


class ExportChatInviteLinkViewSet(ModelViewSet):
    serializer_class = ExportChatInviteLinkSerializer
    queryset = ExportChatInviteLink.objects.all()


class CreateChatInviteLinkViewSet(ModelViewSet):
    serializer_class = CreateChatInviteLinkSerializer
    queryset = CreateChatInviteLink.objects.all()


class EditChatInviteLinkViewSet(ModelViewSet):
    serializer_class = EditChatInviteLinkSerializer
    queryset = EditChatInviteLink.objects.all()


class CreateChatSubscriptionInviteLinkViewSet(ModelViewSet):
    serializer_class = CreateChatSubscriptionInviteLinkSerializer
    queryset = CreateChatSubscriptionInviteLink.objects.all()


class EditChatSubscriptionInviteLinkViewSet(ModelViewSet):
    serializer_class = EditChatSubscriptionInviteLinkSerializer
    queryset = EditChatSubscriptionInviteLink.objects.all()


class RevokeChatInviteLinkViewSet(ModelViewSet):
    serializer_class = RevokeChatInviteLinkSerializer
    queryset = RevokeChatInviteLink.objects.all()


class ApproveChatJoinRequestViewSet(ModelViewSet):
    serializer_class = ApproveChatJoinRequestSerializer
    queryset = ApproveChatJoinRequest.objects.all()


class DeclineChatJoinRequestViewSet(ModelViewSet):
    serializer_class = DeclineChatJoinRequestSerializer
    queryset = DeclineChatJoinRequest.objects.all()


class SetChatPhotoViewSet(ModelViewSet):
    serializer_class = SetChatPhotoSerializer
    queryset = SetChatPhoto.objects.all()


class DeleteChatPhotoViewSet(ModelViewSet):
    serializer_class = DeleteChatPhotoSerializer
    queryset = DeleteChatPhoto.objects.all()


class SetChatTitleViewSet(ModelViewSet):
    serializer_class = SetChatTitleSerializer
    queryset = SetChatTitle.objects.all()


class SetChatDescriptionViewSet(ModelViewSet):
    serializer_class = SetChatDescriptionSerializer
    queryset = SetChatDescription.objects.all()


class PinChatMessageViewSet(ModelViewSet):
    serializer_class = PinChatMessageSerializer
    queryset = PinChatMessage.objects.all()


class UnpinChatMessageViewSet(ModelViewSet):
    serializer_class = UnpinChatMessageSerializer
    queryset = UnpinChatMessage.objects.all()


class UnpinAllChatMessagesViewSet(ModelViewSet):
    serializer_class = UnpinAllChatMessagesSerializer
    queryset = UnpinAllChatMessages.objects.all()


class LeaveChatViewSet(ModelViewSet):
    serializer_class = LeaveChatSerializer
    queryset = LeaveChat.objects.all()


class GetChatViewSet(ModelViewSet):
    serializer_class = GetChatSerializer
    queryset = GetChat.objects.all()


class GetChatAdministratorsViewSet(ModelViewSet):
    serializer_class = GetChatAdministratorsSerializer
    queryset = GetChatAdministrators.objects.all()


class GetChatMemberCountViewSet(ModelViewSet):
    serializer_class = GetChatMemberCountSerializer
    queryset = GetChatMemberCount.objects.all()


class GetChatMemberViewSet(ModelViewSet):
    serializer_class = GetChatMemberSerializer
    queryset = GetChatMember.objects.all()


class SetChatStickerSetViewSet(ModelViewSet):
    serializer_class = SetChatStickerSetSerializer
    queryset = SetChatStickerSet.objects.all()


class DeleteChatStickerSetViewSet(ModelViewSet):
    serializer_class = DeleteChatStickerSetSerializer
    queryset = DeleteChatStickerSet.objects.all()


class CreateForumTopicViewSet(ModelViewSet):
    serializer_class = CreateForumTopicSerializer
    queryset = CreateForumTopic.objects.all()


class EditForumTopicViewSet(ModelViewSet):
    serializer_class = EditForumTopicSerializer
    queryset = EditForumTopic.objects.all()


class CloseForumTopicViewSet(ModelViewSet):
    serializer_class = CloseForumTopicSerializer
    queryset = CloseForumTopic.objects.all()


class ReopenForumTopicViewSet(ModelViewSet):
    serializer_class = ReopenForumTopicSerializer
    queryset = ReopenForumTopic.objects.all()


class DeleteForumTopicViewSet(ModelViewSet):
    serializer_class = DeleteForumTopicSerializer
    queryset = DeleteForumTopic.objects.all()


class UnpinAllForumTopicMessagesViewSet(ModelViewSet):
    serializer_class = UnpinAllForumTopicMessagesSerializer
    queryset = UnpinAllForumTopicMessages.objects.all()


class EditGeneralForumTopicViewSet(ModelViewSet):
    serializer_class = EditGeneralForumTopicSerializer
    queryset = EditGeneralForumTopic.objects.all()


class CloseGeneralForumTopicViewSet(ModelViewSet):
    serializer_class = CloseGeneralForumTopicSerializer
    queryset = CloseGeneralForumTopic.objects.all()


class ReopenGeneralForumTopicViewSet(ModelViewSet):
    serializer_class = ReopenGeneralForumTopicSerializer
    queryset = ReopenGeneralForumTopic.objects.all()


class HideGeneralForumTopicViewSet(ModelViewSet):
    serializer_class = HideGeneralForumTopicSerializer
    queryset = HideGeneralForumTopic.objects.all()


class UnhideGeneralForumTopicViewSet(ModelViewSet):
    serializer_class = UnhideGeneralForumTopicSerializer
    queryset = UnhideGeneralForumTopic.objects.all()


class UnpinAllGeneralForumTopicMessagesViewSet(ModelViewSet):
    serializer_class = UnpinAllGeneralForumTopicMessagesSerializer
    queryset = UnpinAllGeneralForumTopicMessages.objects.all()


class GetUserChatBoostsViewSet(ModelViewSet):
    serializer_class = GetUserChatBoostsSerializer
    queryset = GetUserChatBoosts.objects.all()


class GetBusinessConnectionViewSet(ModelViewSet):
    serializer_class = GetBusinessConnectionSerializer
    queryset = GetBusinessConnection.objects.all()


class SetMyCommandsViewSet(ModelViewSet):
    serializer_class = SetMyCommandsSerializer
    queryset = SetMyCommands.objects.all()


class DeleteMyCommandsViewSet(ModelViewSet):
    serializer_class = DeleteMyCommandsSerializer
    queryset = DeleteMyCommands.objects.all()


class GetMyCommandsViewSet(ModelViewSet):
    serializer_class = GetMyCommandsSerializer
    queryset = GetMyCommands.objects.all()


class SetMyNameViewSet(ModelViewSet):
    serializer_class = SetMyNameSerializer
    queryset = SetMyName.objects.all()


class GetMyNameViewSet(ModelViewSet):
    serializer_class = GetMyNameSerializer
    queryset = GetMyName.objects.all()


class SetMyDescriptionViewSet(ModelViewSet):
    serializer_class = SetMyDescriptionSerializer
    queryset = SetMyDescription.objects.all()


class GetMyDescriptionViewSet(ModelViewSet):
    serializer_class = GetMyDescriptionSerializer
    queryset = GetMyDescription.objects.all()


class SetMyShortDescriptionViewSet(ModelViewSet):
    serializer_class = SetMyShortDescriptionSerializer
    queryset = SetMyShortDescription.objects.all()


class GetMyShortDescriptionViewSet(ModelViewSet):
    serializer_class = GetMyShortDescriptionSerializer
    queryset = GetMyShortDescription.objects.all()


class SetChatMenuButtonViewSet(ModelViewSet):
    serializer_class = SetChatMenuButtonSerializer
    queryset = SetChatMenuButton.objects.all()


class GetChatMenuButtonViewSet(ModelViewSet):
    serializer_class = GetChatMenuButtonSerializer
    queryset = GetChatMenuButton.objects.all()


class SetMyDefaultAdministratorRightsViewSet(ModelViewSet):
    serializer_class = SetMyDefaultAdministratorRightsSerializer
    queryset = SetMyDefaultAdministratorRights.objects.all()


class GetMyDefaultAdministratorRightsViewSet(ModelViewSet):
    serializer_class = GetMyDefaultAdministratorRightsSerializer
    queryset = GetMyDefaultAdministratorRights.objects.all()


class EditMessageTextViewSet(ModelViewSet):
    serializer_class = EditMessageTextSerializer
    queryset = EditMessageText.objects.all()


class EditMessageCaptionViewSet(ModelViewSet):
    serializer_class = EditMessageCaptionSerializer
    queryset = EditMessageCaption.objects.all()


class EditMessageMediaViewSet(ModelViewSet):
    serializer_class = EditMessageMediaSerializer
    queryset = EditMessageMedia.objects.all()


class EditMessageLiveLocationViewSet(ModelViewSet):
    serializer_class = EditMessageLiveLocationSerializer
    queryset = EditMessageLiveLocation.objects.all()


class StopMessageLiveLocationViewSet(ModelViewSet):
    serializer_class = StopMessageLiveLocationSerializer
    queryset = StopMessageLiveLocation.objects.all()


class EditMessageReplyMarkupViewSet(ModelViewSet):
    serializer_class = EditMessageReplyMarkupSerializer
    queryset = EditMessageReplyMarkup.objects.all()


class StopPollViewSet(ModelViewSet):
    serializer_class = StopPollSerializer
    queryset = StopPoll.objects.all()


class DeleteMessageViewSet(ModelViewSet):
    serializer_class = DeleteMessageSerializer
    queryset = DeleteMessage.objects.all()


class DeleteMessagesViewSet(ModelViewSet):
    serializer_class = DeleteMessagesSerializer
    queryset = DeleteMessages.objects.all()


class SendStickerViewSet(ModelViewSet):
    serializer_class = SendStickerSerializer
    queryset = SendSticker.objects.all()


class GetStickerSetViewSet(ModelViewSet):
    serializer_class = GetStickerSetSerializer
    queryset = GetStickerSet.objects.all()


class GetCustomEmojiStickersViewSet(ModelViewSet):
    serializer_class = GetCustomEmojiStickersSerializer
    queryset = GetCustomEmojiStickers.objects.all()


class UploadStickerFileViewSet(ModelViewSet):
    serializer_class = UploadStickerFileSerializer
    queryset = UploadStickerFile.objects.all()


class CreateNewStickerSetViewSet(ModelViewSet):
    serializer_class = CreateNewStickerSetSerializer
    queryset = CreateNewStickerSet.objects.all()


class AddStickerToSetViewSet(ModelViewSet):
    serializer_class = AddStickerToSetSerializer
    queryset = AddStickerToSet.objects.all()


class SetStickerPositionInSetViewSet(ModelViewSet):
    serializer_class = SetStickerPositionInSetSerializer
    queryset = SetStickerPositionInSet.objects.all()


class DeleteStickerFromSetViewSet(ModelViewSet):
    serializer_class = DeleteStickerFromSetSerializer
    queryset = DeleteStickerFromSet.objects.all()


class ReplaceStickerInSetViewSet(ModelViewSet):
    serializer_class = ReplaceStickerInSetSerializer
    queryset = ReplaceStickerInSet.objects.all()


class SetStickerEmojiListViewSet(ModelViewSet):
    serializer_class = SetStickerEmojiListSerializer
    queryset = SetStickerEmojiList.objects.all()


class SetStickerKeywordsViewSet(ModelViewSet):
    serializer_class = SetStickerKeywordsSerializer
    queryset = SetStickerKeywords.objects.all()


class SetStickerMaskPositionViewSet(ModelViewSet):
    serializer_class = SetStickerMaskPositionSerializer
    queryset = SetStickerMaskPosition.objects.all()


class SetStickerSetTitleViewSet(ModelViewSet):
    serializer_class = SetStickerSetTitleSerializer
    queryset = SetStickerSetTitle.objects.all()


class SetStickerSetThumbnailViewSet(ModelViewSet):
    serializer_class = SetStickerSetThumbnailSerializer
    queryset = SetStickerSetThumbnail.objects.all()


class SetCustomEmojiStickerSetThumbnailViewSet(ModelViewSet):
    serializer_class = SetCustomEmojiStickerSetThumbnailSerializer
    queryset = SetCustomEmojiStickerSetThumbnail.objects.all()


class DeleteStickerSetViewSet(ModelViewSet):
    serializer_class = DeleteStickerSetSerializer
    queryset = DeleteStickerSet.objects.all()


class SendGiftViewSet(ModelViewSet):
    serializer_class = SendGiftSerializer
    queryset = SendGift.objects.all()


class VerifyUserViewSet(ModelViewSet):
    serializer_class = VerifyUserSerializer
    queryset = VerifyUser.objects.all()


class VerifyChatViewSet(ModelViewSet):
    serializer_class = VerifyChatSerializer
    queryset = VerifyChat.objects.all()


class RemoveUserVerificationViewSet(ModelViewSet):
    serializer_class = RemoveUserVerificationSerializer
    queryset = RemoveUserVerification.objects.all()


class RemoveChatVerificationViewSet(ModelViewSet):
    serializer_class = RemoveChatVerificationSerializer
    queryset = RemoveChatVerification.objects.all()


class AnswerInlineQueryViewSet(ModelViewSet):
    serializer_class = AnswerInlineQuerySerializer
    queryset = AnswerInlineQuery.objects.all()


class AnswerWebAppQueryViewSet(ModelViewSet):
    serializer_class = AnswerWebAppQuerySerializer
    queryset = AnswerWebAppQuery.objects.all()


class SavePreparedInlineMessageViewSet(ModelViewSet):
    serializer_class = SavePreparedInlineMessageSerializer
    queryset = SavePreparedInlineMessage.objects.all()


class SendInvoiceViewSet(ModelViewSet):
    serializer_class = SendInvoiceSerializer
    queryset = SendInvoice.objects.all()


class CreateInvoiceLinkViewSet(ModelViewSet):
    serializer_class = CreateInvoiceLinkSerializer
    queryset = CreateInvoiceLink.objects.all()


class AnswerShippingQueryViewSet(ModelViewSet):
    serializer_class = AnswerShippingQuerySerializer
    queryset = AnswerShippingQuery.objects.all()


class AnswerPreCheckoutQueryViewSet(ModelViewSet):
    serializer_class = AnswerPreCheckoutQuerySerializer
    queryset = AnswerPreCheckoutQuery.objects.all()


class GetStarTransactionsViewSet(ModelViewSet):
    serializer_class = GetStarTransactionsSerializer
    queryset = GetStarTransactions.objects.all()


class RefundStarPaymentViewSet(ModelViewSet):
    serializer_class = RefundStarPaymentSerializer
    queryset = RefundStarPayment.objects.all()


class EditUserStarSubscriptionViewSet(ModelViewSet):
    serializer_class = EditUserStarSubscriptionSerializer
    queryset = EditUserStarSubscription.objects.all()


class SendGameViewSet(ModelViewSet):
    serializer_class = SendGameSerializer
    queryset = SendGame.objects.all()


class SetGameScoreViewSet(ModelViewSet):
    serializer_class = SetGameScoreSerializer
    queryset = SetGameScore.objects.all()


class IfComponentSet(ModelViewSet):
    serializer_class = IfComponentSerializer
    queryset = IfComponent.objects.all()


class SwitchComponentSet(ModelViewSet):
    serializer_class = SwitchComponentSerializer
    queryset = SwitchComponent.objects.all()


class CodeComponentSet(ModelViewSet):
    serializer_class = CodeComponent
    queryset = CodeComponent.objects.all()
