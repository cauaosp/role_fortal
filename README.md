# Backend do Rolê Fortal 🌊
### Aplicativo idealizado para centralizar o que está ocorrendo em fortaleza.

### Estrutura de contêineres 🐋
3 Contêineres:
- **Backend-Fetcher**: faz a busca por conteúdo em loop a cada 5min e guarda em JSON num arquivo para o backend-web expôr
- **Backend-Web**: consome o banco JSON e compartilha para outros contêineres via web 
- **Frontend**: consome os dados do backend via web e centraliza o conteúdo para o usuário

### Deployment no kubernetes ☸️
- backend-fetcher.yaml: organiza o POD do fetcher e usa o PVC para persistência de dados. OBS: Devo transformá-lo em CronJob depois.
- backend-web.yaml: organiza o POD do web e consome os dados persistidos no PVC.
- pvc.yaml: solicita um armazenamento para realizar os serviços do backend.
- pv.yaml: cria o armazenamento compatível com pvc
- frontend.yaml: POD do FrontEnd.
---
### 📦 Como rodar
- Precisa do kubectl baixado e o minikube rodando
```
1 - minikube start
2 - eval $(minikube docker-env)
3 - docker build -t roles_fortal_backend:dev backend/
4 - docker build -t roles_fortal_frontend:dev frontend/roles-fortal/
```
Rode o comando: *minikube service frontend* para visualizar o Frontend do projeto.

Pode verificar os pods rodando e outras informações com *kubectl get all*

---
### Conteúdo centralizado 📰
- **Diário do Nordeste**: É o jornal com a **maior tiragem** no Estado do Ceará, com forte cobertura em Fortaleza e região.
- **O Povo**: É o **segundo maior** em circulação no estado e o mais antigo em funcionamento em Fortaleza, fundado em 1928.
- **O Estado**: Tradicional veículo com presença online e impressa, cobrindo política, economia e geral.
- **G1 Ceará**: Portal de notícias vinculado à Rede Globo, com ampla cobertura estadual e capital.
- **GC+**: Portal do grupo R7, conhecido por suas seções de entretenimento, cultura e notícias policiais.
- **Ceará Agora**: Veículo que foca em notícias "bombásticas" e últimos acontecimentos do estado.
- **Tribuna do Ceará**: Um dos jornais mais tradicionais do estado, com atualizações diárias.
- **Portal Terra da Luz**: Focado especificamente em informar os principais acontecimentos da cidade de Fortaleza.
- **A Notícia do Ceará**: Site de últimas notícias completo e confiável para a região.
- **Jornal do Brasil** (ou portais de notícias locais como o **GCMAIS**): Frequentemente citados em listas de mídia local para cobertura de eventos e política.
