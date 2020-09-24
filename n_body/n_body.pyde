# Body'leri barındıran liste
bodies = []
# Evrensel çekim sabiti. Farklı G değerleriyle deneyler yapın. Çok eğlenceli...
G = 2

# Setup fonksiyonu
def setup():
    # bodies listesini global scope'tan al
    global bodies
    # Pencere boyutu 500x500 olsun
    size(500, 500)
    # bodies listesine 5 adet Body at
    bodies = [Body(PVector(random(50, width - 50),
                           random(50, height - 50)), random(25, 75)) for _ in range(5)]

# Draw fonksiyonu
def draw():
    # Arka tarafı siyah yap
    background(0)
    # bodies'in içindeki bütün değerleri içinde döngü.
    # Her bir elementi body adlı değişkene at
    for body in bodies:
        # body'yi göster
        body.show()
        # body'ye kuvvet uygula
        body.apply_force(bodies)

# Body sınıfı
class Body:
    # Constructor metod
    # Pozisyon ve kütleyi başlangıçta zorunlu olarak alır
    def __init__(self, pos, mass):
        # Gelen pozisyon ve kütle değerine ulaşabilmek için birer property oluşturuluyor
        self.pos = pos
        self.mass = mass
        # Hız ve İvme için birer property oluşturuluyor
        self.vel = PVector(0, 0)
        self.acc = PVector(0, 0)
        
    # kenardan sekme metodu
    def bound(self):
        # Sayfanın sağına yahut soluna çarptığında yatay yöndeki hızın yönünğ değiştir
        if not self.mass/4 < self.pos.x < width - self.mass/4:
            self.vel.x *= -1
            
        # Sayfanın üt yahut alt tarafına çarptığında yatay yöndeki hızın yönünğ değiştir
        if not self.mass/4 < self.pos.y < height - self.mass/4:
            self.vel.y *= -1
        
    # kuvvet uygulama metodu
    def apply_force(self, others):
        # İvme değerini sıfırla (resetleme)
        self.acc = PVector(0, 0)
         # diğerleri'in içindeki bütün değerleri içinde döngü.
         # Her bir elementi other adlı değişkene at
        for other in others:
            # bu body (self) ile diğer body (other) aynı değilse.
            if self is not other:
                # Bu ve diğer body arasındaki uzaklığı hesapla
                r = dist(self.pos.x, self.pos.y, other.pos.x, other.pos.y)
                # a = G * m2 / r^2. diğer body'nin bu body'ye uygaladığı ivmenin şiddeti 
                acc_mag = G * other.mass / r**2
                # diğer body'nin bu body'ye uygaladığı ivmenin yönü 
                acc_dir = (other.pos - self.pos).heading()
                # İvmenin şiddeti ve yönünü kullanarak bir vektör oluştur
                acc_vec = PVector(0, 0).fromAngle(acc_dir).setMag(acc_mag)
                # Oluşam vektörü ivme değerine ekle
                self.acc.add(acc_vec)
            
        
    # Gösterme metodu
    def show(self):
        # Kenara çarpmayı denetle
        self.bound()
        # Hareket ettir
        self.move()
        
        # Hızın açısı hesapla
        vel_angle = self.vel.heading()
        # Kutupsaldan, kartesyene dönüşüm yaparak, hız yönünde,
        # bulunduğum yerden 50 piksel uzaklığın koordinatını hesapla
        x = self.pos.x + 50 * cos(vel_angle)
        y = self.pos.y + 50 * sin(vel_angle)
        
        # Bulunduğum yerden, hesaplanan yere bir doğru çiz
        stroke(255, 0, 0)
        strokeWeight(3)
        line(self.pos.x, self.pos.y, x, y)
        
        # body'yi çevresiz, içi beyaz dolu bir daire olarak göster
        noStroke()
        fill(255)
        circle(self.pos.x, self.pos.y, self.mass/2)
        
    # Body'yi hareket ettirme        
    def move(self):        
        # ivmeli hareketi simüle et
        self.acc.limit(5)
        self.vel.add(self.acc)
        self.vel.limit(7)
        self.pos.add(self.vel)
