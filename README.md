[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/TCsOx2bu)

# **!!BITNO!!**  
Pošto nisam mogla da instaliram PyCudu na svoj uređaj, projekat je u ipynb formatu, a kod je u potpunosti pisan i testiran u Google Colaboratory. Međutim, ja sam sredila kod da odgovara VSCode sintaksi, tako da ne mora da se otvara na Google Colabu.  
  
Kako bih dokazala da jedan string za kernele nije posledica neznanja, nego okolnosti van moje kontrole, ispod ću napisati kako bi se kerneli pozvali da sam mogla da koristim VSCode.  
  
    with open("kernel.cu", "r") as f:
        cuda_code = f.read()

    mod = SourceModule(cuda_code)
    code = mod.get_function("kernel_code")
