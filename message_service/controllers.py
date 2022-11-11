from .models import Message
from user_service.models import User
from . import QueryPriorityTypes, QueryStatus
from django.utils import timezone
from django.db.models import F, Q, Subquery, Count, Min
import datetime
import operator

# {
#     "message_text": "I need the loan immediately, pleas approve it.",
#     "user_id": 1
# }

# {
#     "message_text": "I need update in my user Profile",
#     "user_id": 1
# }

# {
#     "message_text": "Please approve my application.",
#     "user_id": 1
# }

def find_staff_for_the_query(query):
    user_qs = User.objects.prefetch_related('assigned_messages').filter(is_staff=True)
    total_staff_count = user_qs.count()
    
    experienced_staffs = user_qs.annotate(
        difftime = timezone.now() - F('created_at')
    ).filter(difftime__gte=datetime.timedelta(seconds=24*3600)*(180)).order_by('created_at').annotate(
        query_count_high_priority = Count('id', filter=(
                Q(assigned_messages__status__in = [QueryStatus.QUERY_RECEIVED, QueryStatus.QUERY_IN_PROGRESS]) 
                & Q(assigned_messages__staff_id=F('id'))
                & Q(assigned_messages__priority = QueryPriorityTypes.HIGH)
            )
        ),
        query_count_medium_priority = Count('id', filter=(
                Q(assigned_messages__status__in = [QueryStatus.QUERY_RECEIVED, QueryStatus.QUERY_IN_PROGRESS]) 
                & Q(assigned_messages__staff_id=F('id'))
                & Q(assigned_messages__priority = QueryPriorityTypes.MEDIUM)
            )
        ),
        query_count_low_priority = Count('id', filter=(
                Q(assigned_messages__status__in = [QueryStatus.QUERY_RECEIVED, QueryStatus.QUERY_IN_PROGRESS]) 
                & Q(assigned_messages__staff_id=F('id'))
                & Q(assigned_messages__priority = QueryPriorityTypes.LOW)
            )
        ),
        total_query_count = Count('id', filter=(
                Q(assigned_messages__status__in = [QueryStatus.QUERY_RECEIVED, QueryStatus.QUERY_IN_PROGRESS]) 
                & Q(assigned_messages__staff_id=F('id'))
            )
        )
    ).order_by('created_at').values('id', 'query_count_high_priority', 'query_count_medium_priority', 'query_count_low_priority', 'total_query_count', 'created_at')
    experienced_staffs_count = experienced_staffs.count()
    min_query_count_for_experienced_staffs = experienced_staffs.values('total_query_count').aggregate(Min('total_query_count'))['total_query_count__min']
    
    unexperienced_staffs = user_qs.annotate(
        difftime = timezone.now() - F('created_at')
    ).filter(difftime__lt=datetime.timedelta(seconds=24*3600)*(180)).order_by('created_at').annotate(
        query_count_high_priority = Count('id', filter=(
                Q(assigned_messages__status__in = [QueryStatus.QUERY_RECEIVED, QueryStatus.QUERY_IN_PROGRESS]) 
                & Q(assigned_messages__staff_id=F('id'))
                & Q(assigned_messages__priority = QueryPriorityTypes.HIGH)
            )
        ),
        query_count_medium_priority = Count('id', filter=(
                Q(assigned_messages__status__in = [QueryStatus.QUERY_RECEIVED, QueryStatus.QUERY_IN_PROGRESS]) 
                & Q(assigned_messages__staff_id=F('id'))
                & Q(assigned_messages__priority = QueryPriorityTypes.MEDIUM)
            )
        ),
        query_count_low_priority = Count('id', filter=(
                Q(assigned_messages__status__in = [QueryStatus.QUERY_RECEIVED, QueryStatus.QUERY_IN_PROGRESS]) 
                & Q(assigned_messages__staff_id=F('id'))
                & Q(assigned_messages__priority = QueryPriorityTypes.LOW)
            )
        ),
        total_query_count = Count('id', filter=(
                Q(assigned_messages__status__in = [QueryStatus.QUERY_RECEIVED, QueryStatus.QUERY_IN_PROGRESS]) 
                & Q(assigned_messages__staff_id=F('id'))
            )
        )
    ).order_by('created_at').values('id', 'query_count_high_priority', 'query_count_medium_priority', 'query_count_low_priority', 'total_query_count', 'created_at')
    unexperienced_staffs_count = unexperienced_staffs.count()
    min_query_count_for_unexperienced_staffs = unexperienced_staffs.values('total_query_count').aggregate(Min('total_query_count'))['total_query_count__min']
    
    if query['priority'] == QueryPriorityTypes.HIGH:

        if min_query_count_for_experienced_staffs == 0:

            for experienced_staff in experienced_staffs:

                if experienced_staff.get('total_query_count') == 0:
                    query['staff'] = User.objects.filter(is_staff=True,pk=experienced_staff.get('id')).first()
                    # print(query['staff'])
                    break
        
        else:
            temp_dict_list = []
            for experienced_staff in experienced_staffs:
                temp_dict = {}
                if experienced_staff.get('total_query_count') == min_query_count_for_experienced_staffs:
                    temp_dict['staff_id'] = experienced_staff.get('id')
                    temp_dict['high_priority_count'] = experienced_staff.get('query_count_high_priority')
                    temp_dict_list.append(temp_dict)
            
            temp_dict_list.sort(key=operator.itemgetter('high_priority_count'))
            query['staff'] = User.objects.filter(is_staff=True,pk=temp_dict_list[0].get('staff_id')).first()

    elif query['priority'] == QueryPriorityTypes.MEDIUM:

        if min_query_count_for_experienced_staffs >= 20:
            if min_query_count_for_unexperienced_staffs == 0:

                for unexperienced_staff in unexperienced_staffs:

                    if unexperienced_staff.get('total_query_count') == 0:
                        query['staff'] = User.objects.filter(is_staff=True,pk=unexperienced_staff.get('id')).first()
                        # print(query['staff'])
                        break
            
            else:
                temp_dict_list = []
                for unexperienced_staff in unexperienced_staffs:
                    temp_dict = {}
                    if unexperienced_staff.get('total_query_count') == min_query_count_for_unexperienced_staffs:
                        temp_dict['staff_id'] = unexperienced_staff.get('id')
                        temp_dict['medium_priority_count'] = unexperienced_staff.get('query_count_medium_priority')
                        temp_dict_list.append(temp_dict)
                
                temp_dict_list.sort(key=operator.itemgetter('medium_priority_count'))
                query['staff'] = User.objects.filter(is_staff=True,pk=temp_dict_list[0].get('staff_id')).first()
        
        else:
            if min_query_count_for_experienced_staffs == 0:

                for experienced_staff in experienced_staffs:

                    if experienced_staff.get('total_query_count') == 0:
                        query['staff'] = User.objects.filter(is_staff=True,pk=experienced_staff.get('id')).first()
                        # print(query['staff'])
                        break
            
            else:
                temp_dict_list = []
                for experienced_staff in experienced_staffs:
                    temp_dict = {}
                    if experienced_staff.get('total_query_count') == min_query_count_for_experienced_staffs:
                        temp_dict['staff_id'] = experienced_staff.get('id')
                        temp_dict['high_priority_count'] = experienced_staff.get('query_count_high_priority')
                        temp_dict_list.append(temp_dict)
                
                temp_dict_list.sort(key=operator.itemgetter('high_priority_count'))
                query['staff'] = User.objects.filter(is_staff=True,pk=temp_dict_list[0].get('staff_id')).first()

    elif query['priority'] == QueryPriorityTypes.LOW:
        if min_query_count_for_unexperienced_staffs == 0:

            for unexperienced_staff in unexperienced_staffs:

                if unexperienced_staff.get('total_query_count') == 0:
                    query['staff'] = User.objects.filter(is_staff=True,pk=unexperienced_staff.get('id')).first()
                    # print(query['staff'])
                    break
        
        else:
            temp_dict_list = []
            for unexperienced_staff in unexperienced_staffs:
                temp_dict = {}
                if unexperienced_staff.get('total_query_count') == min_query_count_for_unexperienced_staffs:
                    temp_dict['staff_id'] = unexperienced_staff.get('id')
                    temp_dict['medium_priority_count'] = unexperienced_staff.get('query_count_high_priority')
                    temp_dict_list.append(temp_dict)
            
            temp_dict_list.sort(key=operator.itemgetter('high_priority_count'))
            query['staff'] = User.objects.filter(is_staff=True,pk=temp_dict_list[0].get('staff_id')).first()

    return query

def create_new_query(data):
    query = {}
    message_text = data.get('message_text')
    query['message_text'] = message_text
    try:
        user_instance = User.objects.get(pk=data.get('user_id'))
    except User.DoesNotExist:
        user_instance = None

    query['user'] = user_instance
    query['status'] = QueryStatus.QUERY_RECEIVED

    high_prority_keywords = ['loan', 'money', 'pay', 'bank']
    medium_prority_keywords = ['approve', 'application']
    high_prority_keywords_present = False
    medium_prority_keywords_present = False

    for keyword in high_prority_keywords:
        if keyword in message_text:
            high_prority_keywords_present = True
            query['priority'] = QueryPriorityTypes.HIGH
            break

    if not high_prority_keywords_present:
        for keyword in medium_prority_keywords:
            if keyword in message_text:
                medium_prority_keywords_present = True
                query['priority'] = QueryPriorityTypes.MEDIUM
                break
    
    if not medium_prority_keywords_present and not high_prority_keywords_present:
        query['priority'] = QueryPriorityTypes.LOW

    find_staff_for_the_query(query)

    query_instance = Message.objects.create(**query)
    
    return query_instance


def update_query(data, query_id):
    try:
        query_instance = Message.objects.get(pk=query_id)
    except Message.DoesNotExist:
        query_instance = None
    
    if not query_instance:
        raise ValueError("Query Doesn't Exists")
    
    if data.get('status')==QueryStatus.QUERY_IN_PROGRESS:
        query_instance.status = QueryStatus.QUERY_IN_PROGRESS
    elif data.get('status')==QueryStatus.QUERY_RESOLVED:
        query_instance.status = QueryStatus.QUERY_RESOLVED
    elif data.get('status')==QueryStatus.QUERY_REJECTED:
        query_instance.status = QueryStatus.QUERY_REJECTED
    
    if data.get('priority'):
        query_instance.priority = data.get('priority')
    
    query_instance.save()

    return query_instance

def fetch_query(query_id):
    try:
        query_instance = Message.objects.get(pk=query_id)
    except Message.DoesNotExist:
        query_instance = None
    
    if not query_instance:
        raise ValueError("Query Doesn't Exists")

    query_data = {}

    query_data['message_text'] = query_instance.message_text
    query_data['status'] = query_instance.status
    query_data['priority'] = query_instance.priority
    query_data['created_At'] = query_instance.created_at

    return query_data


def fetch_assigned_messages_of_staff(filter_params):

    queries = Message.objects.filter(**filter_params)

    querires_list = []

    for query in queries:
        query_data  = {
            'id' : query.id,
            'message_text': query.message_text,
            'status': query.status,
            'priority': query.priority,
            'created_At':query.created_at
        }
        querires_list.append(query_data)

    return querires_list


# {
#     "respond_message_text": "Thanks for reaching out, we will update you soon!",
#     "query_id": 119,
#     "staff_id": 8
# }

# {
#     "respond_message_text": "First Message",
#     "query_id": 119,
#     "staff_id": 8
# }

# {
#     "respond_message_text": "Second Message",
#     "query_id": 119,
#     "staff_id": 8
# }

# {
#     "respond_message_text": "Third Message",
#     "query_id": 119,
#     "staff_id": 8
# }

def respond_to_query(data):
    query_id = data.get('query_id')
    staff_id = data.get('staff_id')
    try:
        query_instance = Message.objects.get(pk=query_id)
    except Message.DoesNotExist:
        query_instance = None

    if not query_instance:
        raise ValueError("Query Doesn't Exists")
    
    if not query_instance.staff.id == staff_id:
        raise ValueError("Sorry, You are not allowd to respond to this message!")

    responded_message_queue = query_instance.metadata.get('responded_message_queue')
    
    if not responded_message_queue:
        responded_message_queue = []

    responded_message = {}
    responded_message['responded_message_text'] = data.get('respond_message_text')
    responded_message['responded_at'] = timezone.now()
    responded_message_queue.append(responded_message)
    
    query_instance.metadata["responded_message_queue"] = responded_message_queue
    query_instance.save()
    
    return query_instance

