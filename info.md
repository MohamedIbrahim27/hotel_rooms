==> pagnayion in fucation :
    def product_list(request):
        product_list=Product.objects.all()
        paginator = Paginator(product_list, 32) # Show 25 contacts per page.
        page_number = request.GET.get('page')
        product_list = paginator.get_page(page_number)
        name = ''
        if 'searchname' in request.GET:
            product_list1=Product.objects.all()
            name = request.GET['searchname']
            if name:
                product_list = product_list1.filter(PRDname__icontains=name)
        context ={'product_list' : product_list}
        return render(request, 'Product/product_list.html',context)

==> pagnayion in class :
    class PropertyList(ListView):
        model=Property
        paginate_by=1

==> templates_pagnayion :
    <ul>
        {% if page_obj.has_previous %}
            <li><a href="?page={{page_obj.previous_page_number}}">&lt;</a></li>
        {% else %}
            <li class="disabled"></li>
        {% endif %}
        {% for i in  paginator.page_range %}
            {% if page_obj.number == i %}
                <li class="active"><span>{{i}}</span></li>
            {% else %}
                <li><a href="?page={{i}}">{{i}}</a></li>
            {% endif %}
        {% endfor %}
        {% if page_obj.has_next  %}
            <li ><a href="?page={{page_obj.next_page_number}}">&gt;</a></li>
        {% else %}
            <li class="disabled"></li>
        {% endif %}
    </ul>

