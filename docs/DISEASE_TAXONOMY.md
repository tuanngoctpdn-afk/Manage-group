# Danh Mục Chuẩn Hóa Sâu Bệnh Trên Cây Mít (Jackfruit Pest & Disease Taxonomy)

Tài liệu này phục vụ **Objective 1 (Task 1.1, Task 1.2)** nhằm phân tích triệu chứng lâm sàng và thiết lập tiêu chí nhận diện cho AI.

---

## 1. Bảng Tiêu Chí Nhận Diện & Nhãn Gán AI (AI Annotation Labels)

| Mã nhãn (Class ID) | Tên sâu / bệnh (Tiếng Việt) | Tên khoa học / Tiếng Anh | Bộ phận gây hại chính | Triệu chứng nhận diện lâm sàng |
| :--- | :--- | :--- | :--- | :--- |
| `JF_HEALTHY` | Cây / Quả khỏe mạnh | Healthy Plant / Fruit | Lá, Thân, Trái | Gai nở đều, vỏ sáng màu, lá xanh mượt, thân nhẵn không vết nứt. |
| `JF_FRUIT_BORER` | Sâu đục trái mít | *Diaphania caesalis* | Quả (Trái) | Lỗ đục trên vỏ quả, đùn phân đen/nâu hạt li ti ra ngoài miệng lỗ, quả biến dạng. |
| `JF_SOFT_ROT` | Bệnh thối mềm / Thối đen trái | *Rhizopus artocarpi* / *Phomopsis* | Quả non & Quả già | Vết bệnh úng nước màu nâu sẫm, lan nhanh, mốc đen phát triển như sợi bông/hạt than. |
| `JF_PHYTOPHTHORA_CANKER` | Bệnh thối gốc chảy mủ / nứt thân | *Phytophthora palmivora* | Gốc, Thân chính | Vỏ thân nứt nẻ, chảy nhựa/mủ màu nâu đỏ sẫm, phần gỗ dưới vỏ bị thâm đen. |
| `JF_MEALYBUG` | Rệp sáp hại mít | *Planococcus lilacinus* | Kẽ gai quả, Cuống, Chồi non | Lớp sáp trắng mịn bám dày đặc ở các kẽ gai của quả hoặc chồi non, tiết mật gây nấm bồ hóng. |
| `JF_LEAF_SPOT` | Bệnh đốm lá mít | *Colletotrichum* sp. / *Cercospora* | Lá | Đốm tròn màu nâu vàng, viền sẫm, tâm hoại tử xám tro rụng thủng lá. |
| `JF_PINK_DISEASE` | Bệnh nấm hồng | *Erythricium salmonicolor* | Cành, Nhánh | Lớp mốc phấn màu hồng/trắng bạc bao quanh vỏ cành, làm khô héo cành lá bên trên. |

---

## 2. Tiêu Chí Phân Loại Phẩm Cấp Trái Thu Hoạch (Task 6.2)

Dựa trên xử lý ảnh quả mít khi thu hoạch:
- **Loại 1 (Grade A - Xuất khẩu)**: Trọng lượng > 9kg, dáng quả tròn đều, gai nở căng đều, không có vết thẹo hoặc dấu đục của sâu, không sượng mủ.
- **Loại 2 (Grade B - Nội địa cao cấp)**: Trọng lượng 6-9kg, quả hơi cong nhẹ, bề mặt có vết gai thưa không đáng kể, không sâu đục.
- **Loại 3 (Grade C - Chế biến/Thịt mít)**: Quả méo mó, có dấu hiệu sẹo lành, kích thước nhỏ (<6kg).
- **Loại loại bỏ (Reject)**: Quả nhiễm nấm thối đen, sâu đục sâu vào lõi múi mít.

