from products.models import Product
from core.slack_bot import send_message_to_slack
from .models import Order_Group
from django.utils import timezone

def payment_complete_notification(order_group_pk):
    order_group = Order_Group.objects.get(pk=order_group_pk)
    order_details = order_group.order_details.all()

    product_name = ''

    if order_details.count() == 1:
        product_name = order_details.first().product.title

    else:
        product_name = f'{order_details.first().product.title} 외 {order_details.count() -1}개'

    args = get_order_message_block(**{
        'time': order_group.create_at,
        'order_management_number': order_group.order_management_number,
        'products':product_name,
        'consumer': f'{order_group.consumer.user.nickname} ({order_group.consumer.user.account_name})',
        'price': f'{order_group.total_price}원',
        'payment_type': order_group.payment_type
    })

    send_message_to_slack('C02P6KGV19D', args)


def get_order_message_block(ptype='complete', **args):
    if ptype == 'cancel':
        pass
    
    return [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*결제완료 알림*"
			}
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": f"*결제일시*\n{args['time']}"
				},
                {
					"type": "mrkdwn",
					"text": f"*주문번호*\n{args['order_management_number']}"
				},
				{
					"type": "mrkdwn",
					"text": f"*상품명*\n{args['products']}"
				},
				{
					"type": "mrkdwn",
					"text": f"*주문자*\n{args['consumer']}"
				},
				{
					"type": "mrkdwn",
					"text": f"*결제 금액*\n{args['price']}"
				},
				{
					"type": "mrkdwn",
					"text": f"*결제방법*\n{args['payment_type']}"
				}
			]
		}
	]


def create_order_group(consumer):
    
    """ [payment_create] order_group 생성 / 주문관리번호 생성 """

    order_group = Order_Group(status="wait", consumer=consumer)
    order_group.save()
    
    # 주문관리번호 생성 및 저장
    order_group.create_order_group_management_number()

    return order_group


def create_order_detail(product, quantity):
    
    """ [payment_create] order_detail 생성 / 주문관리번호 생성 """

    product = Product.objects.get(pk=product_pk)


    



