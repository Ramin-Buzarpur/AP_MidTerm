
import unittest
from resources import Resource, CPU, Storage, HDD, SSD

class ResourcesSuite(unittest.TestCase):
    def test_cpu_construction(self):
        cpu = CPU("Ryzen 7 5800X", "AMD", total=8, allocated=3, cores=8, socket="AM4", power_watts=105)
        self.assertEqual(cpu.name, "Ryzen 7 5800X")
        self.assertEqual(cpu.manufacturer, "AMD")
        self.assertEqual(cpu.total, 8); self.assertEqual(cpu.allocated, 3)
        self.assertEqual(cpu.cores, 8); self.assertEqual(cpu.socket, "AM4"); self.assertEqual(cpu.power_watts, 105)
        self.assertEqual(cpu.category, "CPU")
        self.assertIn("CPU(", repr(cpu)); self.assertIn("CPU(", str(cpu))

    def test_hdd_and_ssd_construction(self):
        hdd = HDD("Barracuda", "Seagate", total=20, allocated=4, capacity_GB=2000, size='3.5\"', rpm=7200)
        ssd = SSD("970 EVO Plus", "Samsung", total=10, allocated=2, capacity_GB=500, interface="PCIe NVMe 3.0 x4")
        self.assertTrue(isinstance(hdd, Storage)); self.assertTrue(isinstance(hdd, Resource))
        self.assertTrue(isinstance(ssd, Storage)); self.assertTrue(isinstance(ssd, Resource))
        self.assertEqual(hdd.capacity_GB, 2000); self.assertEqual(ssd.capacity_GB, 500)
        self.assertEqual(hdd.size, '3.5\"'); self.assertEqual(hdd.rpm, 7200)
        self.assertEqual(ssd.interface, "PCIe NVMe 3.0 x4")
        self.assertEqual(hdd.category, "HDD"); self.assertEqual(ssd.category, "SSD")

    def test_invalid_numbers_and_allocated_exceeds_total(self):
        with self.assertRaises(ValueError):
            CPU("X", "Y", total=1, allocated=2, cores=1, socket="S", power_watts=1)
        with self.assertRaises(TypeError):
            HDD("X", "Y", total=1, allocated=0, capacity_GB="512", size='2.5\"', rpm=7200)
        with self.assertRaises(ValueError):
            SSD("X", "Y", total=-1, allocated=0, capacity_GB=512, interface="PCIe")
        with self.assertRaises(TypeError):
            # Direct instantiation must fail
            _ = Resource("n", "m", 1, 0)  # type: ignore

    def test_claim_and_freeup(self):
        cpu = CPU("i5", "Intel", total=10, allocated=2, cores=6, socket="LGA1700", power_watts=65)
        cpu.claim(3); self.assertEqual(cpu.allocated, 5)
        with self.assertRaises(ValueError): cpu.claim(100)
        with self.assertRaises(ValueError): cpu.freeup(6)
        cpu.freeup(2); self.assertEqual(cpu.allocated, 3)
        for bad in (0, -1):
            with self.assertRaises(ValueError): cpu.claim(bad)
            with self.assertRaises(ValueError): cpu.freeup(bad)

    def test_died_and_purchased(self):
        hdd = HDD("WD Blue", "WD", total=15, allocated=5, capacity_GB=1000, size='3.5\"', rpm=7200)
        hdd.purchased(5); self.assertEqual(hdd.total, 20)
        with self.assertRaises(ValueError): hdd.died(16)   # free = 15 (20-5)
        hdd.died(10); self.assertEqual(hdd.total, 10); self.assertEqual(hdd.allocated, 5)
        for bad in (0, -2):
            with self.assertRaises(ValueError): hdd.purchased(bad)
            with self.assertRaises(ValueError): hdd.died(bad)

    def test_category_property(self):
        ssd = SSD("980 Pro", "Samsung", total=6, allocated=1, capacity_GB=1000, interface="PCIe 4.0 x4")
        self.assertEqual(ssd.category, "SSD")

    def test_repr_and_str(self):
        ssd = SSD("T7", "Samsung", total=2, allocated=1, capacity_GB=2000, interface="USB-C")
        r, s = repr(ssd), str(ssd)
        self.assertIn("SSD(", r); self.assertIn("interface", r)
        self.assertIn("SSD(", s); self.assertIn("interface", s)

if __name__ == "__main__":
    unittest.main(verbosity=2)
