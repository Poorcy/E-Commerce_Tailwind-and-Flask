#!/usr/bin/env python3
"""
產品頁面測試腳本
用於測試產品頁面的變體顯示功能
"""

from app import app, db, Product, ProductVariant
from flask import render_template_string

def test_product_template():
    """測試產品模板的變體顯示"""
    with app.app_context():
        print("=== 測試產品模板 ===")
        
        # 獲取第一個產品
        product = Product.query.first()
        if not product:
            print("沒有找到產品")
            return
        
        print(f"測試產品: {product.name}")
        print(f"變體數量: {len(product.variants)}")
        
        # 測試模板條件
        template_code = """
        {% if product and product.variants %}
        <div>產品有變體</div>
        {% for variant in product.variants %}
            {% if variant.color %}
            <div>顏色: {{ variant.color }}</div>
            {% endif %}
            {% if variant.size %}
            <div>尺寸: {{ variant.size }}</div>
            {% endif %}
        {% endfor %}
        {% else %}
        <div>產品無變體</div>
        {% endif %}
        """
        
        try:
            result = render_template_string(template_code, product=product)
            print("模板渲染結果:")
            print(result)
        except Exception as e:
            print(f"模板渲染錯誤: {e}")
        
        # 測試變體資料
        print("\n變體資料:")
        for variant in product.variants:
            print(f"  - 顏色: '{variant.color}', 尺寸: '{variant.size}'")

def test_color_display():
    """測試顏色顯示邏輯"""
    with app.app_context():
        print("\n=== 測試顏色顯示 ===")
        
        colors = ['紅色', '白色', '黑色', '藍色', '綠色']
        
        for color in colors:
            # 模擬模板邏輯
            if color.lower() == 'red' or color == '紅色':
                bg_color = '#ff0000'
            elif color.lower() == 'blue' or color == '藍色':
                bg_color = '#0000ff'
            elif color.lower() == 'green' or color == '綠色':
                bg_color = '#00ff00'
            elif color.lower() == 'yellow' or color == '黃色':
                bg_color = '#ffff00'
            elif color.lower() == 'black' or color == '黑色':
                bg_color = '#000000'
            elif color.lower() == 'white' or color == '白色':
                bg_color = '#ffffff'
            else:
                bg_color = '#cccccc'
            
            print(f"顏色: {color} -> 背景色: {bg_color}")

if __name__ == "__main__":
    test_product_template()
    test_color_display() 