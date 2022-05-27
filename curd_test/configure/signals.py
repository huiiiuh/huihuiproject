import json

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from apps.configure.utils import cal_ip, iptoint

from apps.configure.models import NetworkArea, IpListDetails


def update_ip_list(network_area):
    try:
        ip_list = eval(network_area.ip_list) if isinstance(network_area.ip_list, str) else network_area.ip_list
        querysetlist = []
        for ip in ip_list:
            min_mask_str, max_mask_str = cal_ip(''.join(ip))
            min_mask = iptoint(min_mask_str)
            max_mask = iptoint(max_mask_str)
            querysetlist.append(
                IpListDetails(ip=''.join(ip), network_area=network_area, min_mask=min_mask, max_mask=max_mask))
        IpListDetails.bulk_create_ip_list_details(querysetlist)
    except:
        raise ValueError("上传的ip_list有误")


@receiver(signal=post_save, sender=NetworkArea)
def network_area_save_to_ip_list(sender, instance, created, **kwargs):
    """
    网络区域创建,跟着创建ip_list_detail
    """
    if created:
        update_ip_list(instance)


@receiver(signal=pre_save, sender=NetworkArea)
def update_network__area_to_ip_list(sender, instance, **kwargs):
    if NetworkArea.objects.filter(id=instance.id).exists():
        old_obj = NetworkArea.get_query_network_area_by_id(instance.id)
        if old_obj.ip_list != instance.ip_list:
            # ip_list更新
            IpListDetails.delete_ip_list_details_by_network_area_id(instance.id)
            update_ip_list(instance)
