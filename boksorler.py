import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

# CSV dosyasını okuma
data = pd.read_csv("boksörler.csv", sep=';')

# 'nakavt_etme' ve 'nakavt_edilme' sütunlarını temizleme
def clean_knockout_data(value):
    """'14 KOs' gibi değerleri sadece sayıya çevirir."""
    if isinstance(value, str):
        match = re.search(r'(\d+)', value)
        return int(match.group(1)) if match else np.nan
    return value

data['nakavt_etme'] = data['nakavt_etme'].apply(clean_knockout_data)
data['nakavt_edilme'] = data['nakavt_edilme'].apply(clean_knockout_data)

# Nakavt oranı, boy ve kol açıklığı gibi sütunları temizleme
data['nakavt oranı'] = data['nakavt oranı'].str.replace('%', '').astype(float)
data['height'] = data['height'].str.extract(r'(\d{3})').astype(float)  # Boyu cm olarak düzenle
data['reach'] = data['reach'].str.extract(r'(\d{3})').astype(float)  # Kol açıklığını cm olarak düzenle

# Sayısal sütunları seçme
numerical_columns = ['age', 'maç sayısı', 'rounds', 'nakavt oranı', 'nakavt_etme', 'nakavt_edilme', 'height', 'reach']
for col in numerical_columns:
    data[col] = pd.to_numeric(data[col], errors='coerce')  # Sayısal olmayanları NaN yap

# NaN değerleri temizleme (yalnızca istatistik için gerekli sütunlarda)
cleaned_data = data[numerical_columns]

# İstatistiksel Özet
for col in numerical_columns:
    print(f"=== {col} İçin İstatistikler ===")
    
    # Eğer sütun tamamen NaN ise, uyarı yazdır
    if cleaned_data[col].isna().all():
        print("Bu sütunda sayısal veri yok (tümü NaN).")
        continue
    
    print(f"Ortalama: {cleaned_data[col].mean():.2f}")
    print(f"Medyan: {cleaned_data[col].median():.2f}")
    try:
        mod_value = cleaned_data[col].mode()
        if len(mod_value) > 0:
            print(f"Mod: {mod_value[0]:.2f}")
        else:
            print("Mod: Bulunamadı")
    except Exception as e:
        print(f"Mod: Hata - {str(e)}")
    print(f"Standart Sapma: {cleaned_data[col].std():.2f}")
    print(f"Varyans: {cleaned_data[col].var():.2f}")
    print()


# 2. En Uzun 10 Boksör (Bar Grafiği)
top_10_tallest = data.nlargest(10, 'height')
plt.figure(figsize=(10, 6))
plt.bar(top_10_tallest['name'], top_10_tallest['height'], color='purple')
plt.title('En Uzun 10 Boksör')
plt.xlabel('Boksör İsmi')
plt.ylabel('Boy (cm)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()



# 3. En Çok Maça Çıkan 10 Boksör (Bar Grafiği)
top_10_matches = data.nlargest(10, 'maç sayısı')
plt.figure(figsize=(10, 6))
plt.bar(top_10_matches['name'], top_10_matches['maç sayısı'], color='blue')
plt.title('En Çok Maça Çıkan 10 Boksör')
plt.xlabel('Boksör İsmi')
plt.ylabel('Maç Sayısı')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# 4. Yaş Dağılımı (Histogram)
plt.figure(figsize=(10, 6))
plt.hist(data['age'].dropna(), bins=10, color='green', edgecolor='black')
plt.title('Boksörlerin Yaş Dağılımı')
plt.xlabel('Yaş')
plt.ylabel('Frekans')
plt.tight_layout()
plt.show()

# 5. Stance Dağılımı (Pie Grafiği)
stance_counts = data['stance'].value_counts()
plt.figure(figsize=(8, 8))
plt.pie(stance_counts, labels=stance_counts.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
plt.title('Stance (Duruş) Dağılımı')
plt.tight_layout()
plt.show()

# 6. Kutu Grafiği (Boxplot): Nakavt Oranı
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# CSV dosyasını okuma
data = pd.read_csv("boksörler.csv", sep=';')

# Nakavt oranı sütununu temizleme
data['nakavt oranı'] = data['nakavt oranı'].str.replace('%', '').astype(float)  # Nakavt oranını yüzde olmadan float'a çevir

# NaN değerleri temizleme
data = data.dropna(subset=['nakavt oranı'])

# 1. Nakavt Oranı Dağılımı (Boxplot)
plt.figure(figsize=(10, 6))
sns.boxplot(x=data['nakavt oranı'], color='lightblue')
plt.title('Nakavt Oranının Dağılımı')
plt.xlabel('Nakavt Oranı (%)')
plt.tight_layout()
plt.show()

# 2. En Yüksek Nakavt Oranına Sahip 10 Boksör (Bar Grafiği)
top_10_knockout_rate = data.nlargest(10, 'nakavt oranı')
plt.figure(figsize=(10, 6))
plt.bar(top_10_knockout_rate['name'], top_10_knockout_rate['nakavt oranı'], color='orange')
plt.title('En Yüksek Nakavt Oranına Sahip 10 Boksör')
plt.xlabel('Boksör İsmi')
plt.ylabel('Nakavt Oranı (%)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# 3. Nakavt Oranı Dağılımı (Histogram)
plt.figure(figsize=(10, 6))
plt.hist(data['nakavt oranı'], bins=10, color='purple', edgecolor='black')
plt.title('Nakavt Oranlarının Dağılımı')
plt.xlabel('Nakavt Oranı (%)')
plt.ylabel('Boksör Sayısı')
plt.tight_layout()
plt.show()

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re

# CSV dosyasını okuma
data = pd.read_csv("boksörler.csv", sep=';')

# Sütunları temizleme
def clean_knockout_data(value):
    """'14 KOs' gibi değerleri sadece sayıya çevirir."""
    if isinstance(value, str):
        match = re.search(r'(\d+)', value)
        return int(match.group(1)) if match else None
    return value

# 'nakavt_etme' ve 'nakavt_edilme' sütunlarını temizleme
data['nakavt_etme'] = data['nakavt_etme'].apply(clean_knockout_data)
data['nakavt_edilme'] = data['nakavt_edilme'].apply(clean_knockout_data)

# Nakavt oranı, boy ve kol açıklığı gibi sütunları temizleme
data['nakavt oranı'] = data['nakavt oranı'].str.replace('%', '').astype(float)
data['height'] = data['height'].str.extract(r'(\d{3})').astype(float)
data['reach'] = data['reach'].str.extract(r'(\d{3})').astype(float)

# Sayısal sütunları seçme
numerical_columns = ['age', 'maç sayısı', 'rounds', 'nakavt oranı', 'nakavt_etme', 'nakavt_edilme', 'height', 'reach']
numerical_data = data[numerical_columns].dropna()  # Eksik değerleri temizle

# Korelasyon matrisi
correlation_matrix = numerical_data.corr()

# Konsola yazdırma
print("Korelasyon Matrisi:")
print(correlation_matrix)

# Korelasyon Matrisi Görselleştirme (Heatmap)
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Korelasyon Matrisi (Isı Haritası)")
plt.tight_layout()
plt.show()
