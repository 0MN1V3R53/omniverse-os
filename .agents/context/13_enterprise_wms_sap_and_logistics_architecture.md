# CONTEXT 13: ENTERPRISE WMS, SAP & LOGISTICS ARCHITECTURE

## 1. SAP S/4HANA Enterprise Integration Pipeline
- **OData & REST APIs**: Integration with SAP Core OData services (e.g. `API_SALES_ORDER_SRV`, `API_MATERIAL_DOCUMENT_SRV`, `API_PURCHASEORDER_PROCESS_SRV`).
- **RFC / BAPI Execution**: Node.js/Python RFC connectors (`node-rfc`, `PyRFC`) communicating via SAP NetWeaver RFC SDK for real-time BAPI calls (e.g., `BAPI_GOODSMVT_CREATE`, `BAPI_OUTB_DELIVERY_CREATE_SLS`).
- **IDoc (Intermediate Document) Handling**:
  - Inbound & Outbound EDI/IDoc processing (e.g., `ORDERS05`, `DELVRY07`, `WMMBID02`).
  - Strict XML/flat-file schema validation, dead-letter queuing, and automated retry mechanisms.

---

## 2. Warehouse Management System (WMS) Lifecycle Architecture

```
[Inbound ASN / PO] ➔ [Receiving & Inspection] ➔ [Directed Putaway (Bin Allocation)]
                                                                  │
                                                                  ▼
[Outbound Dispatch] ⬅ [Packing & Manifest] ⬅ [Wave Picking] ⬅ [Storage Inventory]
```

- **Inbound Goods Receipt**:
  - ASN (Advanced Shipping Notice) parsing and barcode matching.
  - Automated inspection, quality check flags, and quarantine bin routing.
- **Directed Putaway & Bin Management**:
  - Dynamic bin selection algorithms: cubic capacity, weight limits, velocity (ABC analysis), hazard classes, and SKU affinity.
  - Hierarchical location model: `Warehouse` ➔ `Zone` ➔ `Aisle` ➔ `Rack` ➔ `Shelf` ➔ `Bin`.
- **Wave Picking & Packing**:
  - Batch, zone, and cluster wave picking strategies to minimize picker travel time.
  - Verification scanning at pick, pack, and palletization stages.
  - Carrier rate-shopping and automated shipping manifest label generation (ZPL / EPL for Zebra thermal printers).

---

## 3. High-Throughput Barcode & RFID Ingestion Engine
- **Hardware Integration**: Industrial handheld terminals (Zebra, Honeywell Android EMDK), fixed RFID portal readers (LLRP protocol).
- **Latency Invariant**: Sub-200ms scan-to-acknowledgement roundtrip over warehouse Wi-Fi/mesh networks.
- **Offline Resiliency**: Client-side SQLite/DataStore queueing with monotonic timestamping and idempotent server deduplication (`UUID` idempotency keys).
- **Symbologies Supported**: Code 128, GS1-128, DataMatrix, QR Code, EPC Gen2 UHF RFID.

---

## 4. Inventory Ledger & Distributed Transaction Invariants
- **ACID Double-Entry Inventory Tracking**:
  - Every stock movement must balance: $\Delta \text{Bin}_{\text{source}} + \Delta \text{Bin}_{\text{destination}} = 0$.
- **Stock Status Dimensions**: Available, Allocated, In-Transit, Damaged, Quality-Hold / Quarantined.
- **Concurrency & Locking**: Optimistic concurrency control (OCC) with version tags on inventory rows to prevent pick-race conditions.
- **Saga Distributed Transaction Coordinator**:
  - Compensating transactions for cross-system fulfillment failures between SAP ERP and local WMS nodes.
