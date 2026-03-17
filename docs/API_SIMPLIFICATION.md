# Uproszczenia API fraq - Changelog

## Nowe funkcje uproszczone (v0.2.11+)

### 1. `generate()` - najprostsze generowanie danych

```python
from fraq import generate

# Zamiast: root + schema + add_field + records...
# Teraz jedna linia:
records = generate({
    'temp': 'float:10-40',      # 10-40°C
    'humidity': 'float:0-100',   # 0-100%
    'sensor_id': 'str',
}, count=100)
```

### 2. `stream()` - strumieniowanie

```python
from fraq import stream

# Strumieniowanie z opóźnieniem
for record in stream({'temp': 'float:0-50'}, count=1000, interval=0.1):
    print(record)
```

### 3. `quick_schema()` - szybkie schemy

```python
from fraq import quick_schema

# Auto-detekcja typów i transformacji
schema = quick_schema('temp', 'humidity', 'pressure')
records = list(schema.records(count=10))
```

### 4. `FraqSchema()` bez root

```python
from fraq import FraqSchema

# Auto-tworzenie root z domyślnymi parametrami
schema = FraqSchema()  # Nie potrzeba: root=FraqNode(...)
schema.add_field('value', 'float')
records = list(schema.records(count=10))  # Uproszczone: count zamiast depth
```

## Przed vs Po (przykłady)

### Przed (stare API):
```python
from fraq import FraqSchema, FraqNode

root = FraqNode(position=(0.0, 0.0, 0.0))  # Trzeba tworzyć ręcznie
schema = FraqSchema(root=root)
schema.add_field('temp', 'float', transform=lambda v: round(float(v) * 40, 1))
schema.add_field('humidity', 'float', transform=lambda v: round(float(v) * 100, 1))
samples = []
for i, record in enumerate(schema.records(depth=3, branching=4)):
    if i >= 100:
        break
    samples.append(record)
```

### Po (nowe uproszczone API):
```python
from fraq import generate

records = generate({
    'temp': 'float:10-40',
    'humidity': 'float:0-100',
}, count=100)
```

**Redukcja kodu: 12 linii → 4 linie (66% mniej)**

## Zmiany w bibliotece

### `fraq/core.py`:
1. `FraqSchema.root` - teraz opcjonalny (auto-created)
2. `FraqSchema.records()` - nowy parametr `count` (łatwiejszy niż depth)
3. `FraqSchema.record()` - transform przed casting (naprawia błędy typów)
4. `_cast()` - uproszczone konwersje (str/int/float)

### `fraq/__init__.py`:
Dodano nowe funkcje:
- `generate()` - generowanie z dict field specs
- `stream()` - lazy streaming
- `quick_schema()` - auto-detekcja typów

## Nowe przykłady

### Uproszczone przykłady Python:
```python
# ai_ml/simple_training_data.py
from fraq import generate
records = generate({'feature_1': 'float', 'label': 'bool'}, count=100)

# iot/simple_sensor_examples.py  
for record in stream({'temp': 'float:10-40'}, count=50):
    print(record)

# etl/simple_pipeline_examples.py
schema = quick_schema('user_id', 'amount', 'status')
```

### Przykłady bash z NLP:
```bash
# nlp_examples.sh
fraq nl 'generuj 100 rekordów sensorów temperatura wilgotność'
fraq nl 'pokaż fraktal głębokość 3 format json'
fraq nl 'znajdź 10 plików pdf w folderze domowym'
```

## Kompatybilność wsteczna

Stare API nadal działa:
```python
# To nadal działa:
root = FraqNode(position=(0.0, 0.0, 0.0))
schema = FraqSchema(root=root)  # Jawny root
schema.records(depth=3, branching=4)  # Depth-based
```

Nowe API jest opcjonalne - dodano jako convenience layer.

## Podsumowanie

| Aspekt | Przed | Po | Zmiana |
|--------|-------|-----|--------|
| Min. linii (simple) | 12 | 4 | -66% |
| Wymagana wiedza | root, depth, branching | count, fields | uproszczone |
| Auto-transformacje | nie | tak (range hints) | +feature |
| Type casting | problematyczny | naprawiony | fix |
| Streaming | ręczny | `stream()` | +function |

Wszystkie nowe funkcje eksportowane przez `from fraq import ...`
