from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import date

# Base para as classes do SQLAlchemy
Base = declarative_base()

# Tabela para armazenar as categorias obrigatórias e bônus da cesta
class Categoria(Base):
    __tablename__ = 'categorias'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String, unique=True, nullable=False) # Ex: 'Arroz', 'Feijão', 'Óleo de soja'
    
    # Relacionamento com a tabela de produtos
    produtos = relationship("Produto", back_populates="categoria")

# Tabela para armazenar os itens extraídos do Giassi via Web Scraping
class Produto(Base):
    __tablename__ = 'produtos'
    
    id = Column(Integer, primary_key=True)
    categoria_id = Column(Integer, ForeignKey('categorias.id'), nullable=False)
    nome_marca = Column(String, nullable=False)
    preco_unitario = Column(Float, nullable=False)
    medida_unidade = Column(String, nullable=False) # Ex: '1kg', '900ml'
    data_coleta = Column(Date, default=date.today, nullable=False)
    
    categoria = relationship("Categoria", back_populates="produtos")

# Tabela para a série histórica do IPCA
class IPCA(Base):
    __tablename__ = 'ipca_historico'
    
    id = Column(Integer, primary_key=True)
    data_referencia = Column(Date, nullable=False, unique=True)
    valor_mensal = Column(Float, nullable=False)
    
# Configuração do motor do banco de dados (SQLite local)
# O parâmetro echo=False evita poluir o terminal, mas você pode mudar para True se quiser ver o SQL gerado
engine = create_engine('sqlite:///dados_cesta_basica.db', echo=False)

def criar_banco():
    print("Criando o schema do banco de dados...")
    Base.metadata.create_all(engine)
    print("Banco de dados 'dados_cesta_basica.db' criado com sucesso!")

if __name__ == "__main__":
    criar_banco()