from django import template
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

register = template.Library()


@register.simple_tag(takes_context=True)
# 这个装饰器表明这个函数是一个模板标签，takes_context = True
# 表示接收上下文对象，就是前面所说的封装了各种变量的 Context 对象。
def paginate(context, obj_list, obj_count):
    left = 3
    right = 3
    # paginator 的分页器
    paginator = Paginator(obj_list, obj_count)
    page = context['request'].GET.get('page')

    try:
        obj_list = paginator.page(page)
        context['current_page'] = int(page)
        pages = page_left(context['current_page'], left, paginator.num_pages) + \
                page_right(context['current_page'], right, paginator.num_pages)
    except PageNotAnInteger:
        obj_list = paginator.page(1)
        context['current_page'] = 1
        pages = page_right(context['current_page'], right, paginator.num_pages)
    except EmptyPage:
        obj_list = paginator.page(paginator.num_pages)
        context['current_page'] = paginator.num_pages
        pages = page_left(context['current_page'], left, paginator.num_pages)
    # 注意 pages.sort()
    pages.sort()
    context['articles'] = obj_list
    context['pages'] = pages
    context['last_page'] = paginator.num_pages
    context['first_page'] = 1
    try:
        context['pages_first'] = pages[0]
        context['pages_last'] = pages[-1] + 1
    except IndexError:
        context['pages_first'] = 1
        context['pages_last'] = 2

    # 必须加这个，否则首页会显示个None
    return ''


def page_left(current_page, left, num_pages):
    """
    辅助函数，获取当前页码的值得左边两个页码值，要注意一些细节，
    比如不够两个那么最左取到2，为了方便处理，包含当前页码值，
    比如当前页码值为5，那么pages = [3,4,5]
    """
    if current_page == 1:
        left_list = []
    elif current_page == num_pages:
        left_list = [i for i in range(current_page-left, current_page) if i > 2]
    else:
        left_list = [i for i in range(current_page, current_page-left, -1) if i > 1]
    return left_list


def page_right(current_page, right, num_pages):
    """
    辅助函数，获取当前页码的值得右边两个页码值，要注意一些细节，
    比如不够两个那么最右取到最大页码值。不包含当前页码值。
    比如当前页码值为5，那么pages = [6,7]
    """
    if current_page == num_pages:
        right_list = []
    else:
        right_list = [i for i in range(current_page+right-1, current_page, -1) if i < num_pages]
    return right_list
