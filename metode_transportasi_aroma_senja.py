
import pulp as lp

model = lp.LpProblem("Distribusi_Biji_Kopi", lp.LpMinimize)

gudang = ["Cimahi", "BuahBatu", "Majalaya"]
cabang = ["Dago", "Cihampelas", "Antapani", "Sukajadi", "Pasteur"]

supply = {"Cimahi":120, "BuahBatu":100, "Majalaya":80}
demand = {"Dago":50, "Cihampelas":60, "Antapani":40, "Sukajadi":30, "Pasteur":20}

cost = {
    ("Cimahi","Dago"):1200, ("Cimahi","Cihampelas"):1300, ("Cimahi","Antapani"):1500,
    ("Cimahi","Sukajadi"):1600, ("Cimahi","Pasteur"):1700,
    ("BuahBatu","Dago"):1400, ("BuahBatu","Cihampelas"):1200, ("BuahBatu","Antapani"):1100,
    ("BuahBatu","Sukajadi"):1500, ("BuahBatu","Pasteur"):1600,
    ("Majalaya","Dago"):1600, ("Majalaya","Cihampelas"):1500, ("Majalaya","Antapani"):1400,
    ("Majalaya","Sukajadi"):1200, ("Majalaya","Pasteur"):1100
}

x = lp.LpVariable.dicts("x", (gudang, cabang), lowBound=0)

model += lp.lpSum(cost[(i,j)] * x[i][j] for i in gudang for j in cabang)

for i in gudang:
    model += lp.lpSum(x[i][j] for j in cabang) <= supply[i]

for j in cabang:
    model += lp.lpSum(x[i][j] for i in gudang) == demand[j]

model.solve()

for i in gudang:
    for j in cabang:
        if x[i][j].varValue > 0:
            print(f"{i} -> {j} = {x[i][j].varValue} kg")

print("Total Biaya =", lp.value(model.objective))
